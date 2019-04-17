# ChrisToolbox
A script to display useful networking and host information

By Chris Morris

For Unix-Based Operating Systems

Requires Python 3.5 or Higher

<br><br>

<h2>Installations</h2>

<h3> Python3 Dependencies </h3>

<code> pip3 install -r requirements.txt </code>


<h3>Required Programs</h3>

<b> dig, screenfetch, net-tools </b>

<i>Usually requires to be run as sudo </i>
  
<h4> Debian </h>

<code> apt install dnsutils net-tools screenfetch </code>


<h4> RHEL </h4>

<code> yum install bind-utils net-tools screenfetch </code>

<h4> Arch Linux </h4>

<code> pacman -S bind-tools net-tools screenfetch </code>


<h2> Parameters </h2>
<i> Usage: ChrisToolbox.py [-h] [-c] [-a] [-s] [-sc] [-i] [-r] [-e] </i> <br>

| Parameter     | Optional Parameter| Information  |
| ------------- |:-------------:| -----:|
| -c            | --credits      | Display Credits | <br>
| -a            | --allnetworking| Display general networking info <br>
| -s            | --networkstats | Display networking stats <br>
| -sc           | --subnetchart  | Display subnets chart <br>
| -i            | --sysinfo      | Display host info with screenfetch <br>
| -r            | --routing      | Display routing table <br>
| -e            | --everything   | Displays all Information <br>



