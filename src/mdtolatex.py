import re

def mdtolatex(text: str) -> str:
    setup = """\\documentclass[a4paper, 11pt]{report}
\\usepackage[french]{babel} % Pour la langue française
\\usepackage{graphicx} % Required for inserting images
\\usepackage{fancyhdr}
\\usepackage[T1]{fontenc}
\\usepackage{amsmath}
\\usepackage{amssymb}
\\usepackage{lipsum}   % Pour générer du texte de remplissage
\\usepackage{caption}
\\usepackage{appendix}
\\usepackage{lmodern}
\\usepackage[a4paper,tmargin=1in,bmargin=1in,lmargin=1in,rmargin=1in]{geometry}
\\usepackage{hyperref}
\\usepackage{xcolor}
\\usepackage{listings}

% Colors for the hyperref package
\\definecolor{urlcolor}{rgb}{0,.145,.698}
\\definecolor{linkcolor}{rgb}{.71,0.21,0.01}
\\definecolor{citecolor}{rgb}{.12,.54,.11}


% color def
\\definecolor{darkred}{rgb}{0.6,0.0,0.0}
\\definecolor{darkgreen}{rgb}{0,0.50,0}
\\definecolor{darkblue}{rgb}{0,0,0.5}
\\definecolor{lightblue}{rgb}{0.0,0.42,0.91}
\\definecolor{orange}{rgb}{0.99,0.48,0.13}
\\definecolor{grass}{rgb}{0.18,0.80,0.18}
\\definecolor{pink}{rgb}{0.97,0.15,0.45}
\\definecolor{backcolour}{rgb}{0.94,0.93,0.92}
\\definecolor{purple}{rgb}{0.58,0,0.82}
\\definecolor{codegreen}{rgb}{0,0.7,0}



% General Setting of listings
\\lstset{
    aboveskip=1em,
    breaklines=true,
    abovecaptionskip=-6pt,
    captionpos=b,
    escapeinside={\\%*}{*)},
    frame=single,
    rulecolor=\\color{backcolour},
    framexleftmargin=2pt, % Adjust left margin
    %frameshape={RYR}{Y}{Y}{RYR}
}

% 0. Basic Color Theme
\\lstdefinestyle{colored}{ %
  basicstyle=\\ttfamily,
  backgroundcolor=\\color{darkred},
  commentstyle=\\color{green},
  keywordstyle=\\color{blue}\\bfseries,
  stringstyle=\\color{red},
}

% 1. General Python Keywords List
\\lstdefinelanguage{PythonPlus}[]{Python}{
  morekeywords=[1]{,as,assert,nonlocal,with,yield,self,True,False,None,} % Python builtin
  morekeywords=[2]{,__init__,__add__,__mul__,__div__,__sub__,__call__,__getitem__,__setitem__,__eq__,__ne__,__nonzero__,__rmul__,__radd__,__repr__,__str__,__get__,__truediv__,__pow__,__name__,__future__,__all__,}, % magic methods
  morekeywords=[3]{,object,type,isinstance,copy,deepcopy,zip,enumerate,reversed,list,set,len,dict,tuple,range,xrange,append,execfile,real,imag,reduce,str,repr,}, % common functions
  morekeywords=[4]{,Exception,NameError,IndexError,SyntaxError,TypeError,ValueError,OverflowError,ZeroDivisionError,}, % errors
  morekeywords=[5]{,ode,fsolve,sqrt,exp,sin,cos,arctan,arctan2,arccos,pi, array,norm,solve,dot,arange,isscalar,max,sum,flatten,shape,reshape,find,any,all,abs,plot,linspace,legend,quad,polyval,polyfit,hstack,concatenate,vstack,column_stack,empty,zeros,ones,rand,vander,grid,pcolor,eig,eigs,eigvals,svd,qr,tan,det,logspace,roll,min,mean,cumsum,cumprod,diff,vectorize,lstsq,cla,eye,xlabel,ylabel,squeeze,}, % numpy / math
}
% 2. New Language based on Python
\\lstdefinelanguage{PyBrIM}[]{PythonPlus}{
  emph={d,E,a,Fc28,Fy,Fu,D,des,supplier,Material,Rectangle,PyElmt},
}
% 3. Extended theme
\\lstdefinestyle{colorEX}{
  basicstyle=\\ttfamily,
  backgroundcolor=\\color{white},
  commentstyle=\\color{darkgreen}\\slshape,
  keywordstyle=\\color{blue}\\bfseries\\itshape,
  keywordstyle=[2]\\color{blue}\\bfseries,
  keywordstyle=[3]\\color{grass},
  keywordstyle=[4]\\color{red},
  keywordstyle=[5]\\color{orange},
  stringstyle=\\color{darkred},
  emphstyle=\\color{pink}\\underbar,
}

\\lstdefinestyle{python}{
    backgroundcolor=\\color{backcolour},
    commentstyle=\\color{codegreen},
    keywordstyle=\\color{pink},
    basicstyle=\\ttfamily\\footnotesize,
    breakatwhitespace=false,
    breaklines=true,
    captionpos=b,
    keepspaces=true,
    showspaces=false,
    showstringspaces=false,
    showtabs=false,
    language=PyBrIM,
}

\\sloppy

\\definecolor{delim}{RGB}{20,105,176}
\\definecolor{numb}{RGB}{106, 109, 32}
\\definecolor{string}{rgb}{0.64,0.08,0.08}

% JSON language style
\\lstdefinelanguage{json}{
    showspaces=false,
    showtabs=false,
    breaklines=true,
    postbreak=\\raisebox{0ex}[0ex][0ex]{\\ensuremath{\\color{gray}\\hookrightarrow\\space}},
    breakatwhitespace=true,
    basicstyle=\\ttfamily\\small,
    upquote=true,
    morestring=[b]",
    stringstyle=\\color{string},
    literate=
     *{0}{{{\\color{numb}0}}}{1}
      {1}{{{\\color{numb}1}}}{1}
      {2}{{{\\color{numb}2}}}{1}
      {3}{{{\\color{numb}3}}}{1}
      {4}{{{\\color{numb}4}}}{1}
      {5}{{{\\color{numb}5}}}{1}
      {6}{{{\\color{numb}6}}}{1}
      {7}{{{\\color{numb}7}}}{1}
      {8}{{{\\color{numb}8}}}{1}
      {9}{{{\\color{numb}9}}}{1}
      {\\{}{{{\\color{delim}{\\{}}}}{1}
      {\\}}{{{\\color{delim}{\\}}}}}{1}
      {[}{{{\\color{delim}{[}}}}{1}
      {]}{{{\\color{delim}{]}}}}{1},
    backgroundcolor=\\color{backcolour},
    breakatwhitespace=false,
    captionpos=b,
    keepspaces=true,
    showstringspaces=false
}

\\lstdefinestyle{json}{
  language = json,
}

\\lstdefinestyle{bash}{
  backgroundcolor=\\color{backcolour},
  commentstyle=\\color{codegreen},
  keywordstyle=\\color{pink},
  basicstyle=\\ttfamily\\footnotesize,
  breakatwhitespace=false,
  breaklines=true,
  captionpos=b,
  keepspaces=true,
  showspaces=false,
  showstringspaces=false,
  showtabs=false,
  language=bash,
}


% To number sections up to subsubsections
\\setcounter{secnumdepth}{3}

% Setup hyperref package
\\hypersetup{
  breaklinks=true,  % so long urls are correctly broken across lines
  colorlinks=true,
%  urlcolor=urlcolor,
  urlcolor=blue,
  linkcolor=black,
  citecolor=citecolor,
}

\\urlstyle{same} % To set the same font for urls as the surrounding text

\\renewcommand{\\appendixpagename}{Annexes}
\\renewcommand{\\appendixtocname}{Annexes}

\\title{Titre du Document}
\\author{Auteur}
\\date{\\today}

\\pagestyle{fancy}
\\fancyhf{} % Nettoie les en-têtes et pieds de page
\\fancyhead[L]{UTC - A25} % En-tête gauche
\\fancyhead[C]{\\leftmark} % En-tête centre
\\fancyhead[R]{TN09} % En-tête droite
\\fancyfoot[C]{\\thepage} % Numéro de page en bas à droite

% Ajuster l'espacement après les paragraphes pour aller à la ligne
\\let\\oldparagraph\\paragraph
\\renewcommand{\\paragraph}[1]{\\oldparagraph{#1}\\mbox{}\\par}

% Permettre les sauts de ligne dans les en-têtes
\\renewcommand{\\chaptermark}[1]{\\markboth{\\thechapter.\\ #1}{}}
\\renewcommand{\\sectionmark}[1]{\\markright{\\thesection.\\ #1}}

% Mettre en valeur le texte en italique (à des fins de débug seulement, pour savoir ce qu'il reste à modifier)
%\\renewcommand{\\emph}[1]{\\emph{\\color{red}#1}}


\\begin{document}

\\begin{titlepage}
    \\centering

    \\includegraphics[width=0.55\\textwidth]{images/utc-logo.png}

    \\vspace*{1cm}

    \\includegraphics[width=0.55\\textwidth]{images/medialab-logo.png}

    \\vfill

    {\\Huge\\bfseries Science des données et fouille du web : collecte, traitement, exploration visuelle et analyse}\\\\[1cm]
    {\\Large Sciences Po médialab}\\\\

    {\\Large TN09 -- Stage Assistant Ingénieur -- Génie Informatique\\\\
    Université de Technologie de Compiègne \\\\[1cm]}

    {\\Large Semestre A25 -- 2 Février 2026}\\\\[1cm]
    {\\Large\\bfseries Auteur :}\\\\[0.3cm]
    {\\Large Evan Chevalérias}\\\\[0.5cm]
    {\\Large\\bfseries Maître de stage :}\\\\[0.3cm]
    {\\Large Guillaume Plique}\\\\[0.5cm]
    {\\Large\\bfseries Suiveur UTC :}\\\\[0.3cm]
    {\\large Marc Shawky}

    \\vspace*{\\fill}
\\end{titlepage}


"""

    regex_patterns = {
        r'^> (.*)$' : r'\\emph{\1}', # Blockquotes to italics
        r'^# Table des matières$' : r'\n\\tableofcontents\n\\cleardoublepage\n\\markboth{}{}',
        r'^# Annexes$' : r'\\appendix\n\\appendixpage\n\\addappheadtotoc\n',
        r'^## Introduction$' : r'\\section*{Introduction}\n\\label{sec:Introduction}',
        r'^# (.{30,50}) (.{30,})$': r'\\chapter{\1 \2}\n\\chaptermark{\1\\protect\\\\\2}\\label{sec:\1 \2}',
        r'^# (.*)$': r'\\chapter{\1}\n\\label{sec:\1}',
        r'^## (.*)$': r'\\section{\1}\n\\label{sec:\1}',
        r'^### (.*)$': r'\\subsection{\1}\n\\label{sec:\1}',
        r'^#### (.*)$': r'\\subsubsection{\1}\n\\label{sec:\1}',
        r'^##### (.*)$': r'\\paragraph{\1}\n\\label{sec:\1}',
        r'\\label\{sec:([^ `",:\*\}]*)[ `",:\*]([^\}]*)\}': r'\\label{sec:\1-\2}', #replace some chars with dash in labels
        r'\[\^(?P<foo>.*)\](.*)\s*\[\^(?P=foo)\]: (.*)\n': r'\\footnote{\3}\2\n', # Footnotes
        r'==(.*)==': r'\1', # Highlighting (no direct LaTeX equivalent)
        r'^\[\/\/\]: # \((.*)\)$' : r'% \1', # Markdown comments to LaTeX comments
        # r'^%%(.*(?:\n.*)*)%%$' : r'% \1', # Alternative Markdown comments to LaTeX comments
        r'^<!--(.*)-->$' : r'% \1', # HTML comments to LaTeX comments
        r'\[([^\[\]]*)\]\(([^\(\)]*)\)' : r'\\href{\2}{\1}', # Markdown links to LaTeX href
        r'^!\[\[([^\]]*)\]\]\n([^\n]*)' : r'\\begin{figure}[h]\n\\centering\n\\includegraphics[width=1.0\\textwidth,height=0.6\\textheight,keepaspectratio]{images/\1}\n\\caption{\2}\n\\label{fig:\1}\n\\end{figure}', # Images with caption
        r'\[\[([^\]]*\.png)\]\]' : r'\\ref{fig:\1}', # Citing figure
        r'\[\[([^#]*)#([^\[\]\|]*)\]\]' : r'[[\1#\2|\2]]', # Internal links to LaTeX references without custom text to custom text
        r'\[\[([^#]*)#([^ `",:\*]*)[ `",:\*]([^\[\]]*)\]\]' : r'[[\1#\2-\3]]', #replace some chars with dash in internal links
        r'\[\[[^#]*#([^\|]*)\|[^\[\]]*\]\]' : r'\\ref{sec:\1}', # Internal links to LaTeX references with custom text
        r'^(.*)\*\*\*(.*)\*\*\*(.*)$': r'\1\\textbf{\\textit{\2}}\3', # Bold and Italic text
        r'^(.*)\*\*(.*)\*\*(.*)$': r'\1\\textbf{\2}\3', # Bold text
        r'^(.*)\*(.*)\*(.*)$': r'\1\\textit{\2}\3', # Italic text
        # r'^(.*)\*([^\*\n]*)\*(.*)$': r'\1\\emph{\\color{red}\2}\3', # Italic text
        r'\n\\\+' : '\n+', # Unescape plus signs at start of line
        r'^```([^\n]*)\n((?:(?!```).|\s)*)\n```' : r'\\begin{lstlisting}[style=\1]\n\2\n\\end{lstlisting}', # Code blocks
        r'`([^`\n]*)`' : r'\\texttt{\1}', # Inline code
        # r'\\texttt\{([^\}\\]*)\_([^\}]*)\}' : r'\\texttt{\1\\\_\2}', # Escape % signs in inline code
        r'\\texttt\{([^\}\\]*)\$([^\}]*)\}' : r'\\texttt{\1\\$\2}', # Escape % signs in inline code
        r'\\texttt\{([^\}\\]*)\&([^\}]*)\}' : r'\\texttt{\1\\\&\2}', # Escape % signs in inline code
        # r'\\texttt\{([^\}\\]*)\%([^\}]*)\}' : r'\\texttt{\1\%\2}', # Escape % signs in inline code
        r'\$\$([^\$]+)\$\$' : r'\\[\1\\]', # Display math
        r'(?<!\\)\$([^\$\n]+)\$' : r'\\(\1\\)', # Inline math
        r'(?<!\{)(https?://[^\s\)\]\}]+)' : r'\\url{\1}', # Plain URLs
        # r'^- (.*)$': r'    \\item \1', # List items
        # r'(?<!\\begin\{itemize\}\n)((?:    \\item [^\n]*\n)+)(?!\\end\{itemize\})': r'\\begin{itemize}\n\1\\end{itemize}\n', # Itemize environment
    }

    for pattern, replacement in regex_patterns.items():
        while re.search(pattern, text, flags=re.MULTILINE):
            text = re.sub(pattern, replacement, text, flags=re.MULTILINE)

    # Escape special LaTeX characters except in math mode and in verbatim environments
    in_math_mode_or_code_mode = False
    passed_toc = False
    at_beginning_of_line = True
    inside_itemize = False
    i = 0
    while i < len(text):

      if not passed_toc and text[i:i+8] == '\\section':
        text = text[:i+8] + '*'+ text[i+8:]
        i += 9
      elif not passed_toc and text[i:i+16] == '\\tableofcontents':
        passed_toc = True
        i += 16
      elif text[i:i+18] == '\\begin{lstlisting}' or text[i:i+16] == '\\end{lstlisting}':
        in_math_mode_or_code_mode = not in_math_mode_or_code_mode
        i += 16 if text[i:i+16] == '\\end{lstlisting}' else 18

      elif text[i:i+2] == '\\(' or text[i:i+2] == '\\)' or text[i:i+2] == '\\[' or text[i:i+2] == '\\]':
        in_math_mode_or_code_mode = not in_math_mode_or_code_mode
        i += 2
      elif not in_math_mode_or_code_mode and not at_beginning_of_line and text[i] in ['&', '%', '_']:
        text = text[:i] + '\\' + text[i:]
        i += 1
      elif at_beginning_of_line and text[i] in ['+', '-']:
        if not inside_itemize:
          text = text[:i] + '\\begin{itemize}\n\\item ' + text[i+2:]
          inside_itemize = True
          i += 20
        else:
          text = text[:i] + '\\item ' + text[i+2:]
          i += 2
      elif at_beginning_of_line and inside_itemize and text[i] not in ['+', '-']:
        text = text[:i] + '\\end{itemize}\n' + text[i:]
        inside_itemize = False
        i += 2


      at_beginning_of_line = (text[i] == '\n')

      i += 1
    return setup + text + "\n\n\\end{document}\n"