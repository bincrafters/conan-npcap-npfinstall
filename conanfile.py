from conans import ConanFile, tools, os


class NpcapNpfinstallConan(ConanFile):
    name = "npcap-npfinstall"
    version = "0.93"
    license = "NPCAP License"
    url = "https://github.com/bincrafters/conan-npcap"
    source_url = "https://github.com/nmap/npcap"
    settings = "arch", "compiler", "build_type"  
    lib_parent_name = "npcap"
    sln_path = os.path.join("packetWin7", "npfinstall", "npfinstall.sln")
    default_options = "configuration=Release"
    options = {
        "configuration": 
            [
                "Release(WinPcap Mode)",
                "Release"
            ] 
    }
    
    def source(self):
        tools.get("{0}/archive/v{1}.zip".format(self.source_url, self.version))

    def build(self):
        vcvars = tools.vcvars_command(self.settings)
        self.run(vcvars)
        unzip_dir = "{0}-{1}".format(self.lib_parent_name, self.version)
        sln_path_full = os.path.join(unzip_dir, self.sln_path)
        build_command = tools.msvc_build_command(self.settings, sln_path_full,  targets=["Build"])
        final_build_command = build_command.replace("Release", '"{0}"'.format(str(self.options.configuration)))
        self.run(final_build_command)

    def package(self):
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = [self.name]
        self.cpp_info.libs = self.collect_libs()
