# first usefull line: 440
page_orig = """<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<html>
  
  <head>
  <style>
  tt { font-family: monospace; font-size: 100%; }
  p.editing { font-family: monospace; margin: 10px; text-indent: -10px; word-wrap:break-word;}
  p { word-wrap: break-word; }
  </style>
  <meta http-equiv="content-type" content="text/html; charset=utf-8">
  <meta name="keywords" content="OEIS,integer sequences,Sloane" />
  
  
  <title>id:A000001 - OEIS</title>
  <link rel="search" type="application/opensearchdescription+xml" title="OEIS" href="/oeis.xml">
  <script>
  var myURL = "\/search?fmt=data\x26q=id:A000001"
  function redir() {
      var host = document.location.hostname;
      if(host != "oeis.org" && host != "127.0.0.1" && host != "localhost" && host != "localhost.localdomain") {
          document.location = "https"+":"+"//"+"oeis"+".org/" + myURL;
      }
  }
  function sf() {
      if(document.location.pathname == "/" && document.f) document.f.q.focus();
  }
  </script>
  </head>
  <body bgcolor=#ffffff onload="redir();sf()">
    <table border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr><td width="100%" align="right">
      <font size=-1>
      
        <a href="/login?redirect=%2fsearch%3ffmt%3ddata%26q%3did%3aA000001">login</a>
      
      </font>
    <tr height=5><td>
    </table>

    <center>
<span style="font-family: sans-serif; font-size: 83%; font-style: italic"><a href="http://oeisf.org">The OEIS Foundation</a> is supported by donations from users of the OEIS and by a grant from the Simons Foundation.</span>
    <br>
<p style="margin-top:-24px">&nbsp;</p>
<a href="/"><img border="0" width="600" height="110" src="/banner2021.jpg" alt="Logo"></a>
    <br>
<p>


<font color="green" ><strong>
</strong></font>


<br>


    <!-- no special fonts -->
    </center>
  
    <center>
    <table border="0" cellspacing="0" cellpadding="0">
      <tr><td>
        
    
    <center>
        <form name=f action="/search" method="GET">
            <table cellspacing=0 cellpadding=0 border=0>
            <tr><td>
            <input maxLength=1024 size=55 name=q value="id:A000001" title="Search Query">
            <input type=hidden name=sort value="">
            <input type=hidden name=language value="">
            <input type=submit value="Search" name=go>
            <td width=10><td>
            <font size=-2><a href="/hints.html">Hints</a></font>
            <tr><td colspan=2>
            <font size=-1>
                (Greetings from <a href="/welcome">The On-Line Encyclopedia of Integer Sequences</a>!)
            </font>
            </table>
        </form>
    </center>

    

    
    <span dir="LTR">Search:</span> <b>id:a000001</b>
    <br>
    
    
    
    
    
    <table bgcolor="#FFFFCC" width="100%" cellspacing="0" cellpadding="0" border="0">
        <tr height="1" bgcolor="#7F7F66"><td>
        <tr><td>
            <table width="100%" cellspacing="0" cellpadding="0" border="0">
                <tr>
                    
                        <td>Displaying 1-1 of 1 result found.
                    
                
                
    
    
    
    <td align=right>
        <font size=-1>page
        
        
            
            
                1
            
        
        
        
        </font>
    

                
            </table>
        <tr><td>
            &nbsp;&nbsp;&nbsp;&nbsp;
            
    
                <font size=-1>Sort:
                
                    
                    
                        relevance
                    
             
                     | 
                    
                        <a href="/search?q=id%3aA000001&fmt=data&sort=references">references</a>
                    
             
                     | 
                    
                        <a href="/search?q=id%3aA000001&fmt=data&sort=number">number</a>
                    
             
                     | 
                    
                        <a href="/search?q=id%3aA000001&fmt=data&sort=modified">modified</a>
                    
             
                     | 
                    
                        <a href="/search?q=id%3aA000001&fmt=data&sort=created">created</a>
                    
             
             </font>
             
             &nbsp;&nbsp;&nbsp;&nbsp;
             
             <font size=-1>Format:
                
                    
                    
                        <a href="/search?q=id%3aA000001">long</a>
                    
             
                     | 
                    
                        <a href="/search?q=id%3aA000001&fmt=short">short</a>
                    
             
                     | 
                    
                        data
                    
             
             </font>
        
        <tr height=1 bgcolor="#7F7F66"><td>
        <tr height=5 bgcolor="#FFFFFF"><td>
    </table>
    
    
    
        
    <table width="750" width="100%" cellspacing="0" cellpadding="0" border="0">
        <tr height="1"><td>
        <tr height=1 bgcolor="#76767F"><td>

        
        <tr bgcolor="#EEEEFF"><td valign=top>
            <table width="100%" cellspacing="0" cellpadding="0" border="0">
                <tr>
                    <td valign=top align=left width=100>
                    
                        <a href="/A000001">A000001</a>
                    
                    
                    <td width=5>
                    <td valign=top align=left>
                    Number of groups of order n.
                    <br><font size=-1>(Formerly M0098 N0035)</font>
                    
                    <td width=2>
                    <td valign=top align=right>
                        <font size=-2>
                        
                            +0<br>
                        
                        164
                        </font>
            </table>
        
            
                
    
    
    
    <tr><td valign=top>
        <table cellspacing="0" cellpadding="2" cellborder="0">
            <tr>
                <td width="20">
                <td width="710">
                    <tt>0, 1, 1, 1, 2, 1, 2, 1, 5, 2, 2, 1, 5, 1, 2, 1, 14, 1, 5, 1, 5, 2, 2, 1, 15, 2, 2, 5, 4, 1, 4, 1, 51, 1, 2, 1, 14, 1, 2, 2, 14, 1, 6, 1, 4, 2, 2, 1, 52, 2, 5, 1, 5, 1, 15, 2, 13, 2, 2, 1, 13, 1, 2, 4, 267, 1, 4, 1, 5, 1, 4, 1, 50, 1, 2, 3, 4, 1, 6, 1, 52, 15, 2, 1, 15, 1, 2, 1, 12, 1, 10, 1, 4, 2</tt>
                    
                        <font size=-1>(<a href="/A000001/list">list</a>;
                        
                        
                        
                            <a href="/A000001/graph">graph</a>;
                        
                        <a href="/search?q=A000001+-id:A000001">refs</a>;
                        <a href="/A000001/listen">listen</a>;
                        <a href="/history?seq=A000001">history</a>;
                        
                        <a href="/search?q=id:A000001&fmt=text">text</a>;
                        <a href="/A000001/internal">internal format</a>)
                        </font>
                    
        </table>
    <tr><td valign=top>
        <table cellspacing="0" cellpadding="2" cellborder="0">
        
            
        
            
        
            
        
            
                 
                 
                 
                 
            
        
            
                 
                 
                 
                 
            
        
            
                 
                 
                 
                 
            
        
            
                 
                 
                 
                 
            
        
            
                 
                 
                 
                 
            
        
            
                 
                 
                 
                 
            
        
            
                 
                 
                 
                 
            
        
            
                 
                 
                 
                 
            
        
            
                 
                 
                 
                 
            
        
            
                 
                 
                 
                 
            
        
            
                 
                 
                 
                 
            
        
            
                 
                 
                 
                 
            
        
            
                 
                 
                 
                 
            
        
            
                 
                 
                 
                 
            
        
        
        
        </table>

            

        <tr height=10><td>
    </table>

    
    
    
    <table bgcolor="#FFFFCC" width="100%" cellspacing="0" cellpadding="0" border="0">
        <tr height="1" bgcolor="#7F7F66"><td>
        <tr><td>
            <table width="100%" cellspacing="0" cellpadding="0" border="0">
                <tr>
                
    
    
    
    <td align=right>
        <font size=-1>page
        
        
            
            
                1
            
        
        
        
        </font>
    

            </table>
        <tr height=1 bgcolor="#7F7F66"><td>
    </table>
    
    
    <center><p><font size=-1>
      Search completed in 0.505 seconds
    </font></p></center>

      </td></tr>
    </table>
    </center>
    
    <p>
    
    <center>
      <a href="/">Lookup</a> |
      <a href="/wiki/Welcome"><font color="red">Welcome</font></a> |
      <a href="/wiki/Main_Page"><font color="red">Wiki</font></a> |
      <a href="/wiki/Special:RequestAccount">Register</a> |
      
      <a href="/play.html">Music</a> |
      <a href="/plot2.html">Plot 2</a> |
      <a href="/demo1.html">Demos</a> |
      <a href="/wiki/Index_to_OEIS">Index</a> |
      <a href="/Sbrowse.html">Browse</a> |
      <a href="/more.html">More</a> |
      <a href="/webcam">WebCam</a>
      
      <br>
      
      <a href="/Submit.html">Contribute new seq. or comment</a> |
      <a href="/eishelp2.html">Format</a> |
      <a href="/wiki/Style_Sheet">Style Sheet</a> |
      <a href="/transforms.html">Transforms</a> |
      <a href="/ol.html">Superseeker</a> |
      <a href="/recent">Recent</a> 
      
      <br>
      
      <a href="/community.html">The OEIS Community</a> |
      Maintained by <a href="http://oeisf.org">The OEIS Foundation Inc.</a> 
    </center>

    <p>
    <center>
   <span style="font-family: sans-serif; font-size: 83%; font-style: italic">
    <a href="/wiki/Legal_Documents">
    License Agreements, Terms of Use, Privacy Policy.
    </a>.
    </span>
    </center>

    <p>
    <center>
    <font size=-1>Last modified March 20 11:48 EDT 2021.  Contains 342301 sequences. (Running on oeis4.)</font>
    </center>
    <p>
    
  </body>
</html>"""

from urllib import request
import re
def header(id):
    """Download title from HTML of the sequence of given id."""
    
    search = request.urlopen(f'https://oeis.org/search?q=id:{id}&fmt=data')
    header_length = 1000  # number of characters in header.
    header = search.read(header_length).decode()
    # print(header)
    total = int(re.findall(
        "Displaying \d+-\d+ of (\d+) results found.", header)[0])
    print(total)
print(f'dsa{"a12"}att')

# source page:
page = """
   <tr>
                    <td valign=top align=left width=100>
                    
                        <a href="/A000055">A000055</a>
                    
                    
                    <td width=5>
                    <td valign=top align=left>
                    Number of trees with n unlabeled nodes.
                    <br><font size=-1>(Formerly M0791 N0299)</font>
                    
                    <td width=2>
                    <td valign=top align=right>
                        <font size=-2>
                        
                            +0<br>
         """               
# print(page)
total = re.findall('''<a href=\"/(A\d{6})\">A\d{6}</a>
                    
                    
                    <td width=5>
                    <td valign=top align=left>
		[\w\W]+
                    <td width=2>''', page)
total = re.findall(r'''<a href=\"/A\d{6}\">A\d{6}</a>
                    
                    
                    <td width=5>
                    <td valign=top align=left>
                    ((.+\n)+)[ \t]+<td width=\d+>''', page_orig)
# <td width=2>
# ''', page)
totala = re.findall(r"<a href=\"/A\d{6}\">A\d{6}</a>.*\n((.+\n)+)[ \t]+<td width=2>", page, re.M)
# totala = re.findall(r"<a href=\"/A\d{6}\">A\d{6}</a>\n", page)
# total = re.findall('^[ \t]+<td width=\d>', page, re.M)
# totala = re.findall('<a href=\"/', page)
print(total, len(total))
