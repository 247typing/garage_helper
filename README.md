# garage_helper
A gui to do basic calculations for garage projects. The framework is setup to easily allow for adding more tools at a later date. See the adding a tool section below.
<br/><br/>
## Install Instructions
<pre>
1. Clone from github
2. Install dependencies (Note: currently will not work on linux)
   1. Windows  => pip install -r requirements.txt
   2. Linux    => pip3 install -r requirements.txt
3. Run program
   1. Windows  => python garage_helper.py
   2. Linux    => python3 garage_helper.py
</pre>
<br/><br/>
## Adding a Tool
To add a new tool just follow the steps below.
<pre>
1. Copy the class from dev_tools -> tool_template.py
2. Paste this class in garage_helper.py under the last tool class and above global variables
3. Change the name and nice name.
4. Add wanted tool at bottom but still inside the contructor
5. Comment out the size of other tools and replace with 1
6. Try different sized until the new tool is just the right size
7. Remove the 1's in the other tools and uncomment original values
</pre>
<br/><br/>
This tutorial was very useful for learning a convenient way to use tkinter with classes.
https://pythonprogramming.net/tkinter-depth-tutorial-making-actual-program/
The lathe speeds chart was modified from the one found on wikipedia
https://en.wikipedia.org/wiki/Speeds_and_feeds
