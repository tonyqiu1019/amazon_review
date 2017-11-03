Size =  "small larger love big feels smaller deal compact perfect sturdy narrower screen bag feel heavier laptop good lightweight inches tablet pad computer sleek pounds backlit keyboard weight lighter touch bezel portable easy great nice thin heavy super fast size light backpack width typing inch carry travel lbs "
Graphics =  "play radeon game color angles bright graphics video medium resolution colors viewing integrated saturation high retina games pixel nvidia crisp settings gaming excellent display fps photo ips picture editing sharp quality 1080p brightness reflective build 4k contrast hd matte higher "
Processor =  "dual-core turbo range processors quad-core dualcore gen faster CPU cpu dual cores celeron price beat generation chip 3rd 4th cpu i3 i5 processor intel ivy i7 core pentium quad haswell performance quadcore sandy GHz ghz amd boost bridge atom party duo "
Memory =  "vengeance memory gig crucial RAM memory sodimm dimm 2gb 4gb corsair upgraded total 8gb upgradable 16gb soldered kit stick gb ram c720 upgradable 8gb pc3 upgrade upgradeable ram 4gb module 204-pin ddr2 ddr3 slots sticks gb gigs mhz 2x4gb "
Software =  "installed software update office microsoft updates mac products apple docs web browser operating free apps hardware app os chrome ms chromebook google store windows system pc install xp programs vista user word account "
HardDrive =  "internal data ssd mechanical partitioned recovery storage sata space 500gb sandisk 5400rpm partition dvd seagate 128gb hard msata burner evo 1tb Space partitions cd solid cd/dvd hdd replaced rpm tb 512gb 7200rpm disk external drives disc drive optical raid flash "
Ports =  "wired tv thunderbolt usb reader mic converter dongle slot ports firewire network output vga sd mouse router projector dvi pci connection microphone cable connect wifi adapter adapters mini USB hdmi headphone jack ethernet expresscard bluetooth hub port micro gigabit displayport HDMI wireless card "
Battery =  "shut lasts lifetime turn battery cell supply drain life long sleep mode button unplugged seconds hour advertised saver power takes day plugged waste hours charge minutes spent charging hrs cord longer charges charger phone short time charged "

def switch(x):
    return {
        'Screen Size': Size,
        'Graphics Coprocessor': Graphics,
        'Processor': Processor,
        'RAM': Memory,
        'Operating System': Software,
        'Hard Drive': HardDrive,
        'Number of USB 2.0 Ports': Ports,
        'Number of USB 3.0 Ports': Ports,
        'Average Battery Life (in hours)': Battery
    }.get(x, "")
