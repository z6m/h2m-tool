<h1 align="center">Zom's Funny Server Fetcher</h1>
<h6 align="center">Checks the hashes, fetches your servers, runs your game, you get the idea</h6>
<h5 align="center">Read everything here before tweeting/dming me. I've probably already answered it</h5>

--------------------------------------------------------------------------------------------------------------------

<h6>Designed for the now defunct h2m-mod for Call of Duty Modern Warfare Remastered. This repo is unaffiliated with the team, nor does it contain or aid in the distribution of any files involved with the project. It is meant to validate the authenticity the mod binaries out in the wild that were leaked before the team disbanded and stopped working on the project in order to help prevent people from just downloading and running malware trying to play the game/connect to malicious servers.</h6>

# Important stuff
This is an unsigned executable that reaches out to external servers (github for update checking, iw4.zip for server listings), so an antivirus will probably warn you or quarantine it or something. That tends to happen. You can either allow it through or look over my spaghetti code and compile it yourself (which the .bat lets you do pretty easily if you know basic python).

Also, just because your build of the game is clean doesn't necessarily mean you're 100% safe. Some packages containing the files are known to have additional .msi or .exe files that present themselves as installers for a "launcher". This launcher no longer exists, as the team is no longer continuing the project and their distribution channels have been shut down. The launcher itself is unnecessary for a client to run the mod as it is, and any of them that are packed in with the client-side mod files should be treated as, at best, useless or, at worst, malware (as well as any similar executables beyond h2m-mod.exe, which this project is meant to validate). Server guys, you're on your own with that.


# Setup
1. Go the the [releases](https://github.com/z6m/h2m-tool/releases) tab
2. Download the latest release (the .exe, not any of the zips)
3. Drop it in whatever folder you have your h2m-mod.exe files
4. Make a shortcut of it that you can put on your desktop if you want
5. You are done

Run it instead of the h2m-mod.exe if you always want your servers updated.

# What it actually does
The H2M.exe tool reaches out to github to make sure it's the latest version of itself, then validates the hash of your binary. 

<h5>SAFE: You have the last offical binary that was given to early access participants, this should end in (e33e) and if you're on it you have nothing to worry about at least in terms of your binary </h5>

<h5>OLDER: You have the build from before the final day of the early access that was a part of the first leak, this should end in (e127) and isn't malicious as far as I know; just outdated (see </h5> 

<h5>UNKNOWN: You have some random build that someone from a discord server probably told you has a server browser modded into it. This could contain literally anything and you probably shouldn't run it. This tool fetches servers on startup and completely side steps the need for any modification to the binary to achieve this. Delete whatever you have and use this instead unless you REALLY trust whoever made it and gave it to you.</h5> 


The tool then fetches the latest server list available at [master.iw4.zip](https://master.iw4.zip/servers) and writes them to the favorites.json located in your player folder that can be viewed in the client by clicking "Filter Servers" to set your source to "Favorites". If you're seeing 0 Players and 0 Servers online with your source set to "Internet", good, you're not supposed to.

Upon finishing these two tasks, the tool will run your h2m-mod.exe as normal and close itself. It doesn't need to install anything, run in the background, or act as a replacement for/interact with any game files in any way (meaning if anything breaks after it closes itself, that's on whatever you've got going on). 

# Compiling from source
While the releases are binaries that have been precompiled so they require no outside installs and can be ran on any machine with no technical knowledge required, this is still an open source project. If you don't trust the precompiled binaries, I added a .bat file that will let you easily clone the repo and compile it yourself to make sure the code you're seeing is the code that's running on your machine (you'll obviously need to install python as well as any dependancies yourself). If you're on Linux (I saw you, Steamdeck users) and managed to get h2m working, I trust that you probably know how to run a python script and don't need anything compiled at all.

# Known issues
The game itself only lets you have 100 servers visible in the browser, even when the source is set to internet. This seems to just be an MWR thing

    Solution: planning to refactor the script to pull the top 100 servers with the best ping


-----------------------------------------------------------------------------------------------------------------------------------------------------------------

# FAQ regarding H2M itself

<h3 align="center">"Will this tool give me the mod files?"</h3>
No, this tool is for validation and easy access to a "functioning" server list without modifying any original binaries. This repo contains no copyrighted assets and is purely code written by its contributor(s).

<h3 align="center">"Will YOU give me mod files?"</h3>
<p>No, I would much rather be able to continue helping people without risking getting any of my stuff suspended or getting a C&D of my own and being legally prevented from doing so. I have only ever directly given out mod files before the C&D to my fellow early access gamers or to the people helping me with security research.</p>

<p>That said, you can probably find that exact stuff floating around somewhere. It's a 2.2-2.4gb zip with no maps included, contains "h2m-mod.exe", "h1_mp64_ship.exe", and the "h2m-mod" folder; that's it. Might even have my name in the game logs from when I was playing during early access, hash ends in e33e, check the hashes before running any executable. Game files you'll need to get elsewhere, preferably legally.</p>

<h3 align="center">"What would a working game folder look like?"</h3>
<h6 align="center">Something like this</h6>
<img src="https://github.com/user-attachments/assets/011dce0d-a5ee-458d-9ee6-0b1674b3a29a">

<h3 align="center">"I have the old build, am I cooked? What features am I missing?"</h3>
No, you're probably fine. Would get the new one if you can. And I have no idea exactly what features are missing; I wasn't on the H2M team itself, hence why I'm able to talk about it and help people. The mod was recieveing multiple updates throughout the day involving tweaks to game feel (particularly regarding glides, catwalks, and other associated mechanics). I have no way of knowing exactly what was in each individual build, I just happened to catch the latest one before they shut down the update channel to try to suppress leaks.

<h3 align="center">"Virustotal says the safe build/this tool contains wacatac/wacapew/some other trojan"</h3>
Virustotal/similar AV products are doing behavioral analysis based on what the file does in a vaccuum. "h2m-mod.exe", even the clean version, reaches out to an external server that does not exist anymore (the h2m-mod.dev update server that got shut down) and modifies registry keys related to the game. My tool reaches out to github/master.iw4.zip to check for updates to the version/fetch servers. These are all necessary things the programs would inherently need to do to fulfill their intended purposes and will trigger false positives in behavioral testing as these executables are either unsigned or self-signed meaning they have no inherent trust from any platform.  

<h3 align="center">"I got my exe from __________'s server, who are the new official team for H2M"</h3>
<p>There is no new "official" team for H2M, just collectives of various random people trying to fill the vacuum that was made after the team disbanded. These are often loosely formed groups scrambling to establish themselves as fast as possible. Some of them are probably legitimately trying to build on the project, some of them also see a free program with no official distribution channel that a ton of people want and will take advantage of that; both are equally likely with any tampered build you download. </p>

<h6>The purpose of this tool is to provide the functionality those builds are offering without the need to actually modify the binary itself so no trust in an outside party is required and there's never a question as to what you're actually running. As of right now, there is no reason to use a tampered binary over a clean one with this tool. </h6>

<p>I can't speak on any of their builds and there are known examples (https://x.com/LeafFGC/status/1824708025908859063) of infected files going around. Until this whole the stabilizes, I wouldn't recommend running any of them and just asking them for the early access version they built off of.</p>

<h3 align="center">"I try to connect to a server but it says it's full/it puts me some other random server"</h3>
People are joining and filling up servers a lot faster than the game itself seems to be able to visibly update the list. Combine that with the fact that the browser itself currently only displays 100 servers at a time and that's going to happen sometimes. 
