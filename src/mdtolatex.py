import re

def mdtolatex(text: str) -> str:
    setup = """
\\documentclass[a4paper, 11pt]{report}
\\usepackage{graphicx} % Required for inserting images
\\usepackage{fancyhdr}
\\usepackage[T1]{fontenc}
\\usepackage[french]{babel} % Pour la langue française
\\usepackage{amsmath}
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
\\definecolor{lightblue}{rgb}{0.0,0.42,0.91}
\\definecolor{orange}{rgb}{0.99,0.48,0.13}
\\definecolor{grass}{rgb}{0.18,0.80,0.18}
\\definecolor{pink}{rgb}{0.97,0.15,0.45}

% General Setting of listings
\\lstset{
  aboveskip=1em,
  breaklines=true,
  abovecaptionskip=-6pt,
  captionpos=b,
  escapeinside={\\%*}{*)},
  frame=single,
  numbers=left,
  numbersep=15pt,
  numberstyle=\\tiny,
}
% 0. Basic Color Theme
\\lstdefinestyle{colored}{ %
  basicstyle=\\ttfamily,
  backgroundcolor=\\color{white},
  commentstyle=\\color{green}\\itshape,
  keywordstyle=\\color{blue}\\bfseries\\itshape,
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


% To number sections up to subsubsections
\\setcounter{secnumdepth}{3}

% Setup hyperref package
\\hypersetup{
  breaklinks=true,  % so long urls are correctly broken across lines
  colorlinks=true,
%  urlcolor=urlcolor,
  urlcolor=blue,
  linkcolor=linkcolor,
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
"""

    regex_patterns = {
        r'^---\n((?:(?!---).)*)\n---$': '',
        r'^# (.*)$': r'\\chapter{\1}\n\\label{sec:\1}',
        r'^## (.*)$': r'\\section{\1}\n\\label{sec:\1}',
        r'^### (.*)$': r'\\subsection{\1}\n\\label{sec:\1}',
        r'^#### (.*)$': r'\\subsubsection{\1}\n\\label{sec:\1}',
        r'^##### (.*)$': r'\\paragraph{\1}\n\\label{sec:\1}',
        r'\n\\label\{sec:([^ \}]*)[ `",:]([^\}]*)\}': r'\n\\label{sec:\1-\2}', #replace some chars with dash in labels
        r'\[\^(?P<foo>.*)\](.*)\s*\[\^(?P=foo)\]: (.*)\n': r'\\footnote{\3}\2', # Footnotes
        r'==(.*)==': r'\1', # Highlighting (no direct LaTeX equivalent)
        r'^(.*)\*\*\*(.*)\*\*\*(.*)$': r'\1\\textbf{\\textit{\2}}\3', # Bold and Italic text
        r'^(.*)\*\*(.*)\*\*(.*)$': r'\1\\textbf{\2}\3', # Bold text
        # r'^(.*)\*(.*)\*(.*)$': r'\1\\textit{\2}\3', # Italic text
        r'^(.*)\*([^\*\n]*)\*(.*)$': r'\1\\emph{\\color{red}\2}\3', # Italic text
        r'^\[\/\/\]: # \((.*)\)$' : r'% \1', # Markdown comments to LaTeX comments
        r'!\[\[(.*)\]\]' : r'% \1', # Images
        r'\[([^\[\]]*)\]\(([^\(\)]*)\)' : r'\\href{\2}{\1}', # Markdown links to LaTeX href
        r'\[\[([^#]*)#([^\[\]\|]*)\]\]' : r'[[\1#\2|\2]]', # Internal links to LaTeX references without custom text to custom text
        r'\[\[([^#]*)#([^\| ]*)[ `",:]([^\|]*)\|([^\[\]]*)\]\]' : r'[[\1#\2-\3|\4]]', #replace space with dash in internal links
        r'\[\[[^#]*#([^\|]*)\|([^\[\]]*)\]\]' : r'\\href{sec:\1}{\2}', # Internal links to LaTeX references with custom text
        r'\n\\\+' : '\n+', # Unescape plus signs at start of line
        r'^```([^\n]*)\n((?:(?!```).|\s)*)\n```' : r'\\begin{verbatim}\n\2\n\\end{verbatim}', # Code blocks
        r'`([^`\n]*)`' : r'\\texttt{\1}', # Inline code
        r'\\texttt\{([^\}]*)(?<!\\)\$([^\}]*)\}' : r'\\texttt{\1\\$\2}', # Dollar signs in inline code
        r'\$\$([^\$]+)\$\$' : r'\\[\1\\]', # Display math
        r'(?<!\\)\$([^\$]+)\$' : r'\\(\1\\)', # Inline math
        r'(?<!\{)(https?://[^\s\)\]\}]+)' : r'\\url{\1}', # Plain URLs
        # r'^- (.*)$': r'    \\item \1', # List items
        # r'(?<!\\begin\{itemize\}\n)((?:    \\item [^\n]*\n)+)(?!\\end\{itemize\})': r'\\begin{itemize}\n\1\\end{itemize}\n', # Itemize environment
    }

    for pattern, replacement in regex_patterns.items():
        while re.search(pattern, text, flags=re.MULTILINE):
            text = re.sub(pattern, replacement, text, flags=re.MULTILINE)

    # Escape special LaTeX characters except in math mode
    in_math_mode = False
    at_beginning_of_line = True
    i = 0
    while i < len(text):
      # if text[i] == '\\':
      #   if i + 1 < len(text):
      #     next_char = text[i + 1]
      #     if next_char == '(' or next_char == ')':
      #       in_math_mode = not in_math_mode
      #       i += 1
      #     elif next_char == '[' or next_char == ']':
      #       if i + 2 < len(text) and text[i + 2] == '\\[' or text[i + 2] == '\\]':
      #         in_math_mode = not in_math_mode
      #         i += 3

      if text[i:i+2] == '\\(' or text[i:i+2] == '\\)' or text[i:i+2] == '\\[' or text[i:i+2] == '\\]':
        in_math_mode = not in_math_mode
        i += 2
      elif not in_math_mode and not at_beginning_of_line and text[i] in ['&', '%', '_']:
        text = text[:i] + '\\' + text[i:]
        i += 1
      at_beginning_of_line = (text[i] == '\n')
      i += 1
    return setup + "\n\\begin{document}\n\\maketitle\n\n" + text + "\n\n\\tableofcontents\n\n\\end{document}\n"