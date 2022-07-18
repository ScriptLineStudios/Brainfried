<div align="center">
  <h1>Brainfried - A brainfuck compiler<h1/>
  <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/ScriptLineStudios/Brainfried">
  <img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/ScriptLineStudios/Brainfried">
  <img alt="Lines of code" src="https://img.shields.io/tokei/lines/github/ScriptLineStudios/Brainfried">

  <h1>About</h1>
    <h5>Brainfried is a brainfuck compiler. Which compiles brainfuck code down into x86_64 assembly which can then be compiled using <a href="https://www.nasm.us/">nasm<a/><h5/>
</div>
    


<div align="center">
  <h1>Setup</h1>
  To get started. Install <a href="https://www.nasm.us/">nasm<a/> for your linux distro
</div>
<br>
<pre>
      1. git clone https://github.com/ScriptLineStudios/Brainfried.git
      2. cd Brainfried
      3. pip install .
      4. You can now use the command: "brainfry" for any brainfuck file. Example:
      5. brainfry -r examples/fibb.b
      6. -r is used to run the generated assembly
</pre>
</br>


