import uproot
import hist

# defining some global constants
N1 = 79
N2 = 8
N3 = 25

file_prefix = "uhh2.AnalysisModuleRunner."
base_path = "/nfs/dust/cms/user/flabe/TstarTstar/data/DNN/"

# defining some helper functions
def write_histogram(pname, hin, hout, fout):
    """
    get histogram from input file and write as to output file
    """
    with uproot.open(pname) as fin:
        hist = fin[hin]
        fout[hout] = hist

    return True

def write_hadded_histograms(pnames, hin, hout, fout):
    
    with uproot.open(pnames[0]) as fin:
        hist = fin[hin].to_hist()
        
    for i in range(1, len(pnames)):
        with uproot.open(pnames[i]) as fin:
            hist += fin[hin].to_hist()
        
    fout[hout] = hist

def getCorrelationString(year, correlations):
    correlationstring = ""
    for entry in correlations:
        if(year in entry):
            for year in entry: correlationstring += year
    if correlationstring == "": correlationstring + "not_applicable"
        
    return correlationstring


# defining the main class
class Datacard():

    def __init__(self, year, mass_point, svar, channel, region, processes, norm_uncertainties, shape_uncertanties, spinpostfix = "", doJECJER = True, doPDF_MCscale = True, doDatadriven = True, varyDatadrivenBtagAlone = True):
        self.year = year
        self.mass_point = mass_point
        self.svar = svar
        self.channel = channel
        self.region = region
        self.spinpostfix = spinpostfix
        self.doJECJER = doJECJER
        self.doPDF_MCscale = doPDF_MCscale
        self.varyDatadrivenBtagAlone = varyDatadrivenBtagAlone
        
        self.fname = f"{self.mass_point}_{self.svar}_{self.channel}_{self.region}"
        
        self.doDatadriven = doDatadriven
        
        self.processes = processes.copy()
        if doDatadriven: self.processes.append("datadriven")
        self.generate_datacard(norm_uncertainties, shape_uncertanties)

    def write_block_header(self, f, block_name: str):
        f.write(f"# {block_name.capitalize()}\n")
        f.write(N1 * "-" + "\n")

    def write_parameters(self, f):
        self.write_block_header(f, "parameters")
        f.write(f"imax 1\njmax {len(self.processes)-1}\nkmax *\n")
        f.write(f"shapes * {self.region} {self.fname}{self.spinpostfix}.root "
                f"$PROCESS $PROCESS_$SYSTEMATIC\n\n")

    def write_channels(self, f):
        self.write_block_header(f, "channels")
        f.write(f"bin          {self.region}\n")
        f.write("observation  -1\n\n")

    def pad(self, s, n_pad):
        s = str(s)
        n_pad = n_pad - len(s)
        return s + n_pad * ' '

    def write_processes(self, f):
        padded_processes = [self.pad(x, N3) for x in self.processes]
        padded_ids = [self.pad(i , N3) for i in range(len(self.processes))]
        self.write_block_header(f, "processes")
        f.write(self.pad("bin", N1 + N2) + len(self.processes) * self.pad(self.region, N3) + "\n")
        f.write(self.pad("process", N1 + N2) + "".join(padded_processes) + "\n")
        f.write(self.pad("process", N1 + N2) + "".join(padded_ids) + "\n")
        f.write(self.pad("rate", N1 + N2) + len(self.processes) * self.pad("-1", N3))
        f.write("\n\n")

    def write_lnN_systematics(self, f, norm_uncertainties):
        self.write_block_header(f, "systematics")
        for nuisance in norm_uncertainties:
            f.write(self.pad(nuisance, N1) + self.pad("lnN", 8))
            for process in self.processes:
                if process in norm_uncertainties[nuisance]:
                    np_val = norm_uncertainties[nuisance][process]
                    if isinstance(np_val, dict):
                        np_val = np_val[self.year]
                    f.write(self.pad(np_val, N3))
                else:
                    f.write(self.pad("-", N3))
            f.write("\n")

    def write_shape_systematics(self, f, shape_uncertanties):
        for shape_np in shape_uncertanties:
            applicable_processes = shape_uncertanties[shape_np][0]
            correlations = shape_uncertanties[shape_np][1]
            
            correlationstring = getCorrelationString(self.year, correlations)
            
            f.write(self.pad(shape_np + "_" + correlationstring, N1) + self.pad("shape", 8))
            
            for process in self.processes:
                if (process in applicable_processes):
                    f.write(self.pad(1, N3))
                elif (process == "datadriven" and "btagging" in shape_np):
                    if self.varyDatadrivenBtagAlone:
                        f.write(self.pad("-", N3))
                    else:
                        # varying with the largest if together!
                        if shape_np == "btagging_hf": f.write(self.pad(1, N3))
                        else: f.write(self.pad("-", N3))
                else:
                    f.write(self.pad("-", N3))
            f.write("\n")
            
    def write_JECJER(self, f):
        # both JEC and JER will be treated as uncorrelated between years
        
        correlationstring = self.year
        f.write(self.pad("JEC_" + correlationstring, N1) + self.pad("shape", 8))
        for process in self.processes:
            if process == "datadriven":
                f.write(self.pad("-", N3))
            else:
                f.write(self.pad(1, N3))
        f.write("\n")
        
        f.write(self.pad("JER_" + correlationstring, N1) + self.pad("shape", 8))
        for process in self.processes:
            if process == "datadriven":
                f.write(self.pad("-", N3))
            else:
                f.write(self.pad(1, N3))
        f.write("\n")
        
    def write_PDF_MCscale(self, f):
        # these will be treated as correlated between years, but uncorrelated between samples!
        
        correlationstring = "UL16UL17UL18"
        
        for process in self.processes:
            if process == "datadriven": continue
            f.write(self.pad("PDF_" + process +  "_" + correlationstring, N1) + self.pad("shape", 8))
            for process2 in self.processes:
                if process == process2:
                    f.write(self.pad(1, N3))
                else:
                    f.write(self.pad("-", N3))
            f.write("\n")
                    
        for process in self.processes:
            if process == "datadriven": continue
            f.write(self.pad("scale_" + process +  "_" + correlationstring, N1) + self.pad("shape", 8))
            for process2 in self.processes:
                if process == process2:
                    f.write(self.pad(1, N3))
                else:
                    f.write(self.pad("-", N3))
            f.write("\n")
            
    def write_datadriven(self, f):
        
        # TODO make this configurable from outside maybe?
        datadriven_systs = ["datadrivenFitFunction"]
        if self.varyDatadrivenBtagAlone: datadriven_systs.append("btagging_total")
        
        # these will be correlated through the years, and only apply to datadriven
        
        correlationstring = "UL16UL17UL18"
        
        for datadriven_syst in datadriven_systs:
            
            f.write(self.pad(datadriven_syst + "_" + correlationstring, N1) + self.pad("shape", 8))
            for process in self.processes:
                if process == "datadriven":
                    f.write(self.pad(1, N3))
                else:
                    f.write(self.pad("-", N3))
            f.write("\n")

    def generate_datacard(self, norm_uncertainties, shape_uncertanties):
        with open(f"cards/{self.year}/{self.fname}{self.spinpostfix}.dat", 'w') as f:
            self.write_parameters(f)
            self.write_channels(f)
            self.write_processes(f)
            self.write_lnN_systematics(f, norm_uncertainties)
            self.write_shape_systematics(f, shape_uncertanties)
            if self.doJECJER: self.write_JECJER(f)
            if self.doPDF_MCscale: self.write_PDF_MCscale(f)
            if self.doDatadriven: self.write_datadriven(f)
            f.write("* autoMCStats 0")

    def create_rootfile(self, shape_uncertanties):
        with uproot.recreate(f"cards/{self.year}/{self.fname}{self.spinpostfix}.root") as fout:
            
            shape_path = base_path + self.year + "/hadded/"
            
            if (self.region == "SR"): region_string = "SignalRegion_"
            elif (self.region == "VR"): region_string = "ValidationRegion_"
            else: raise Exception("region not recognized")
            
            shape_folder = region_string + self.channel
        
            # moving the nominal ones
            all_pnames = []
            for process in self.processes:
                if not process == "datadriven":
                    hin_base = shape_folder + "/" + self.svar
                    pname = shape_path + file_prefix + "MC." + process + ".root"
                    all_pnames.append(pname)
                    write_histogram(pname, hin_base + "_nominal", process, fout)
                        
            # data
            hin_base = shape_folder + "/" + self.svar
            pname = shape_path + file_prefix + "DATA.DATA.root"
            write_histogram(pname, hin_base + "_nominal", "data_obs", fout)
                                
                
            # move histograms for "normal" shape systematics
            for shape_np in shape_uncertanties:
                applicable_processes = shape_uncertanties[shape_np][0]
                correlations = shape_uncertanties[shape_np][1]
                
                correlationstring = getCorrelationString(self.year, correlations)
                
                for process in self.processes:
                    if process in applicable_processes:
                        pname = shape_path + file_prefix + "MC." + process + ".root"
                        hin_base = shape_folder + "/" + self.svar
                        write_histogram(pname, hin_base + "_" + shape_np + "Up",
                                        process + "_" + shape_np + "_" + correlationstring + "Up", fout)
                        write_histogram(pname, hin_base + "_" + shape_np + "Down",
                                        process + "_" + shape_np + "_" + correlationstring + "Down", fout)

                    
            # JEC and JER
            if self.doJECJER:
                correlationstring = self.year
                for JE in ["JEC", "JER"]:
                    for direction in ["up", "down"]:
                        JECJER_path = base_path + self.year + "/" + JE + "_" + direction + "/hadded/"

                        for process in self.processes:
                            if not process == "datadriven":
                                hin_base = shape_folder + "/" + self.svar
                                pname = JECJER_path + file_prefix + "MC." + process + ".root"
                                write_histogram(pname, hin_base + "_nominal",
                                                process + "_" + JE + "_" + correlationstring + direction.capitalize(), fout)
            
                        
            # datadriven
            if self.doDatadriven:
                datadriven_base_path = "/nfs/dust/cms/user/flabe/TstarTstar/data/DNN_datadriven"

                correlationstring = self.year
                pname = datadriven_base_path + "/" + self.year + "/hadded/uhh2.AnalysisModuleRunner.DATA.datadrivenBG.root"
                baseline = region_string + self.channel + "/" + self.svar  + "_nominal"
                write_histogram(pname, baseline , "datadriven", fout)

                # datadriven function variations
                variations = region_string + "datadriven_FuncUp_" + self.channel + "/" + self.svar  + "_nominal"
                write_histogram(pname, variations , "datadriven_datadrivenFitFunction_UL16UL17UL18Up", fout)
                variations = region_string + "datadriven_FuncDown_" + self.channel + "/" + self.svar  + "_nominal"
                write_histogram(pname, variations , "datadriven_datadrivenFitFunction_UL16UL17UL18Down", fout)

                datadriven_btag_name = "datadriven_btagging_hf_UL16UL17UL18"
                if self.varyDatadrivenBtagAlone: datadriven_btag_name = "datadriven_btagging_total_UL16UL17UL18"
                
                # datadriven b-tagging variations
                variations = region_string + "datadriven_BtagUp_" + self.channel + "/" + self.svar  + "_nominal"
                write_histogram(pname, variations , datadriven_btag_name + "Up", fout)
                variations = region_string + "datadriven_BtagDown_" + self.channel + "/" + self.svar  + "_nominal"
                write_histogram(pname, variations , datadriven_btag_name + "Down", fout)
            
            # PDF & scale
            if self.doPDF_MCscale:
                external_base_path = "/nfs/dust/cms/user/flabe/TstarTstar/ULegacy/CMSSW_10_6_28/src/UHH2/TstarTstar/macros/rootmakros/files"

                correlationstring = "UL16UL17UL18"
                for what in ["PDF", "scale"]:
                    for process in self.processes:
                        if not process == "datadriven":
                            pname = external_base_path + "/" + what + "/" + region_string + what + "_" + self.year + "_" + self.channel + "_" + process + ".root"
                            write_histogram(pname, process + "_" + what +"_up",
                                                    process + "_" + what + "_" + process + "_" + correlationstring + "Up", fout)
                            write_histogram(pname, process + "_" + what + "_down",
                                                    process + "_" + what + "_" + process + "_" + correlationstring + "Down", fout)
