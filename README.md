# Zom's Funny H2M Server Fetcher
Checks the hashes, fetches your servers, runs your game, you get the idea

Designed for the now defunct h2m-mod for Call of Duty Modern Warfare Remastered. This repo is unaffiliated with the team, nor does it contain or aid in the distribution of any files involved with the project. It is meant to validate the authenticity the mod binaries out in the wild that were leaked before the team disbanded and stopped working on the project in order to help prevent people from just downloading and running malware trying to play the game/connect to malicious servers. 

# Important stuff
This is an unsigned executable that reaches out to external servers (github for update checking, iw4.zip for server listings), so an antivirus will probably warn you or quarantine it or something. That tends to happen. You can either allow it through or look over my spaghetti code and compile it yourself (which the .bat lets you do pretty easily if you know basic python).

Also, just because your build of the game is clean doesn't necessarily mean you're 100% safe. Some packages containing the files are known to have additional .msi or .exe files that present themselves as installers for a "launcher". This launcher no longer exists, as the team is no longer continuing the project and their distribution channels have been shut down. The launcher itself is unnecessary for a client to run the mod as it is, and any of them that are packed in with the client-side mod files should be treated as, at best, useless or, at worst, malware (as well as any similar executables beyond h2m-mod.exe, which this project is meant to validate). Server guys, you're on your own with that.


# Setup
1. Go the the [releases](https://github.com/z6m/h2m-tool/releases) tab
2. Download the latest release (the .exe)
3. Drop it in whatever folder you have your h2m-mod.exe files
4. Make a shortcut of it that you can put on your desktop if you want
5. You are done

Run it instead of the h2m-mod.exe if you always want your servers updated.

# What it actually does
The H2M.exe tool reaches out to github to make sure it's the latest version of itself, then validates the hash of your binary. 

    SAFE: You have the last offical binary that was given to early access participants, this should end in (e33e) and if you're on it you have nothing to worry about at least in terms of your binary
    OLDER: You have the build from before the final day of the early access that was a part of the first leak, this should end in (e127) and isn't malicious as far as I know; just outdated
    UNKNOWN: You have some random build that someone from a discord server probably told you has a server browser modded into it. This could contain literally anything and you probably shouldn't run it. This tool fetches servers on startup and completely side steps the need for any modification to the binary to achieve this. Delete whatever you have and use this instead unless you REALLY trust whoever made it and gave it to you.

The tool then fetches the latest server list available at [master.iw4.zip](https://master.iw4.zip/servers) and writes them to the favorites.json located in your player folder that can be viewed in the client by clicking "Filter Servers" to set your source to "Favorites". If you're seeing 0 Players and 0 Servers online with your source set to "Internet", good, you're not supposed to.

Upon finishing these two tasks, the tool will run your h2m-mod.exe as normal and close itself. It doesn't need to install anything, run in the background, or act as a replacement for/interact with any game files in any way (meaning if anything breaks after it closes itself, that's on whatever you've got going on). 

# Compiling from source
While the releases are binaries that have been precompiled so they require no outside installs and can be ran on any machine with no technical knowledge required, this is still an open source project. If you don't trust the precompiled binaries, I added a .bat file that will let you easily clone the repo and compile it yourself to make sure the code you're seeing is the code that's running on your machine (you'll obviously need to install python as well as any dependancies yourself). If you're on Linux (I saw you, Steamdeck users) and managed to get h2m working, I trust that you probably know how to run a python script and don't need anything compiled at all.
