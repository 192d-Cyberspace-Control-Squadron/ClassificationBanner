using System;
using WixSharp;
using WixSharp.Common;

class Program
{
    static void Main()
    {
        // Path to your existing exe (adjust as needed)
        var exePath = @"..\..\dist\Windows\ClassificationBanner.exe";

        // Install folder: C:\Program Files\Department of War\ClassificationBanner
        var project = new Project(
            "Classification Banner",
            new Dir(
                @"%ProgramFiles%\Department of War\ClassificationBanner",
                new File(exePath),
                // Registry Run key: runs at user logon
                new RegValue(
                    RegistryHive.LocalMachine,
                    @"Software\Microsoft\Windows\CurrentVersion\Run",
                    "ClassificationBanner",
                    "\"[INSTALLDIR]ClassificationBanner.exe\""
                )
            )
        );

        // Basic product metadata
        project.GUID = new Guid("f302f7d2-bd3a-4d3a-886f-243c0ef39a24");
        project.Manufacturer = "Department of War";
        project.Version = new Version("1.3.0.0");

        // Optional: nice output filename
        project.OutFileName = "ClassificationBanner-Setup";

        // Make it per-machine
        project.InstallScope = InstallScope.perMachine;
        project.Platform = Platform.x64;

        // Build the MSI
        Compiler.BuildMsi(project);
    }
}
