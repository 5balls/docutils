#! /usr/bin/env python3
# $Id$
# Author: engelbert gruber <grubert@users.sourceforge.net>
# Copyright: This module has been placed in the public domain.

"""
Tests for latex2e writer.
"""

import os
from pathlib import Path
import string
import sys
import unittest

if __name__ == '__main__':
    # prepend the "docutils root" to the Python library path
    # so we import the local `docutils` package.
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from docutils.core import publish_string

# DATA_ROOT is ./test/data from the docutils root
DATA_ROOT = Path(__file__).resolve().parents[1] / 'data'
spam = os.path.relpath(DATA_ROOT/'spam').replace('\\', '/')
ham = os.path.relpath(DATA_ROOT/'ham.tex').replace('\\', '/')


class WriterPublishTestCase(unittest.TestCase):

    maxDiff = None
    writer_name = 'latex'
    settings = {
        '_disable_config': True,
        'strict_visitor': True,
        # Explicit set current default to avoid latex writer future warnings:
        'use_latex_citations': False,
        'legacy_column_widths': True,
        }

    def test_defaults(self):
        for name, cases in samples_default.items():
            for casenum, (rst_input, expected) in enumerate(cases):
                with self.subTest(id=f'samples_default[{name!r}][{casenum}]'):
                    output = publish_string(source=rst_input,
                                            writer_name=self.writer_name,
                                            settings_overrides=self.settings)
                    self.assertEqual(output.decode('utf-8'), expected)

    def test_docutils_toc(self):
        settings = self.settings.copy()
        settings['use_latex_toc'] = False
        for name, cases in samples_docutils_toc.items():
            for casenum, (rst_input, expected) in enumerate(cases):
                with self.subTest(id=f'samples_docutils_toc[{name!r}][{casenum}]'):
                    output = publish_string(source=rst_input,
                                            writer_name=self.writer_name,
                                            settings_overrides=settings)
                    self.assertEqual(output.decode('utf-8'), expected)

    def test_book(self):
        settings = self.settings.copy()
        settings['documentclass'] = 'book'
        for name, cases in samples_book.items():
            for casenum, (rst_input, expected) in enumerate(cases):
                with self.subTest(id=f'samples_book[{name!r}][{casenum}]'):
                    output = publish_string(source=rst_input,
                                            writer_name=self.writer_name,
                                            settings_overrides=settings)
                    self.assertEqual(output.decode('utf-8'), expected)

    def test_latex_sectnum(self):
        settings = self.settings.copy()
        settings['use_latex_toc'] = False
        settings['sectnum_xform'] = False
        for name, cases in samples_latex_sectnum.items():
            for casenum, (rst_input, expected) in enumerate(cases):
                with self.subTest(
                        id=f'samples_latex_sectnum[{name!r}][{casenum}]'):
                    output = publish_string(source=rst_input,
                                            writer_name=self.writer_name,
                        settings_overrides=settings)
                    self.assertEqual(output.decode('utf-8'), expected)

    def test_latex_citations(self):
        settings = self.settings.copy()
        settings['use_latex_citations'] = True
        for name, cases in samples_latex_citations.items():
            for casenum, (rst_input, expected) in enumerate(cases):
                with self.subTest(
                        id=f'samples_latex_citations[{name!r}][{casenum}]'):
                    output = publish_string(source=rst_input,
                                            writer_name=self.writer_name,
                                            settings_overrides=settings)
                    self.assertEqual(output.decode('utf-8'), expected)

    def test_table_style_auto(self):
        settings = self.settings.copy()
        settings['table_style'] = ['colwidths-auto']
        for name, cases in samples_table_style_auto.items():
            for casenum, (rst_input, expected) in enumerate(cases):
                with self.subTest(
                        id=f'samples_table_style_auto[{name!r}][{casenum}]'):
                    output = publish_string(source=rst_input,
                                            writer_name=self.writer_name,
                                            settings_overrides=settings)
                    self.assertEqual(output.decode('utf-8'), expected)

    def test_booktabs(self):
        settings = self.settings.copy()
        settings['table_style'] = ['booktabs']
        for name, cases in samples_table_style_booktabs.items():
            for casenum, (rst_input, expected) in enumerate(cases):
                with self.subTest(id=f'samples_booktabs[{name!r}][{casenum}]'):
                    output = publish_string(source=rst_input,
                                            writer_name=self.writer_name,
                                            settings_overrides=settings)
                    self.assertEqual(output.decode('utf-8'), expected)

    def test_link_stylesheet(self):
        settings = self.settings.copy()
        settings['stylesheet_path'] = f'{spam},{ham}'
        for name, cases in samples_stylesheet.items():
            for casenum, (rst_input, expected) in enumerate(cases):
                with self.subTest(id=f'samples_link_stylesheet[{name!r}][{casenum}]'):
                    output = publish_string(source=rst_input,
                                            writer_name=self.writer_name,
                                            settings_overrides=settings)
                    self.assertEqual(output.decode('utf-8'), expected)

    def test_embed_embed_stylesheet(self):
        settings = self.settings.copy()
        settings['stylesheet_path'] = f'{spam},{ham}'
        settings['embed_stylesheet'] = True
        settings['warning_stream'] = ''
        for name, cases in samples_stylesheet_embed.items():
            for casenum, (rst_input, expected) in enumerate(cases):
                with self.subTest(id=f'samples_embed_stylesheet[{name!r}][{casenum}]'):
                    output = publish_string(source=rst_input,
                                            writer_name=self.writer_name,
                                            settings_overrides=settings)
                    self.assertEqual(output.decode('utf-8'), expected)

    def test_bibtex(self):
        settings = self.settings.copy()
        settings['use_bibtex'] = ['alpha', 'xampl']
        for name, cases in samples_bibtex.items():
            for casenum, (rst_input, expected) in enumerate(cases):
                with self.subTest(id=f'samples_bibtex[{name!r}][{casenum}]'):
                    output = publish_string(source=rst_input,
                                            writer_name=self.writer_name,
                                            settings_overrides=settings)
                    # print(output.decode('utf-8'))
                    self.assertEqual(output.decode('utf-8'), expected)


head_template = string.Template(
r"""$head_prefix% generated by Docutils <https://docutils.sourceforge.io/>
\usepackage{cmap} % fix search and cut-and-paste in Acrobat
$requirements
%%% Custom LaTeX preamble
$latex_preamble
%%% User specified packages and stylesheets
$stylesheet
%%% Fallback definitions for Docutils-specific commands
$fallbacks$pdfsetup
%%% Body
\begin{document}
$titledata""")

parts = dict(
head_prefix=r"""\documentclass[a4paper]{article}
""",
requirements=r"""\usepackage{ifthen}
\usepackage[T1]{fontenc}
""",
latex_preamble=r"""% PDF Standard Fonts
\usepackage{mathptmx} % Times
\usepackage[scaled=.90]{helvet}
\usepackage{courier}
""",
longtable=r"""\usepackage{longtable,ltcaption,array}
\setlength{\extrarowheight}{2pt}
\newlength{\DUtablewidth} % internal use in tables
""",
stylesheet='',
fallbacks='',
fallbacks_highlight=r"""
% basic code highlight:
\providecommand*\DUrolecomment[1]{\textcolor[rgb]{0.40,0.40,0.40}{#1}}
\providecommand*\DUroledeleted[1]{\textcolor[rgb]{0.40,0.40,0.40}{#1}}
\providecommand*\DUrolekeyword[1]{\textbf{#1}}
\providecommand*\DUrolestring[1]{\textit{#1}}

% custom inline roles: \DUrole{#1}{#2} tries \DUrole#1{#2}
\providecommand*{\DUrole}[2]{%
  \ifcsname DUrole#1\endcsname%
    \csname DUrole#1\endcsname{#2}%
  \else%
    #2%
  \fi%
}
""",
pdfsetup=r"""
% hyperlinks:
\ifthenelse{\isundefined{\hypersetup}}{
  \usepackage[colorlinks=true,linkcolor=blue,urlcolor=blue]{hyperref}
  \usepackage{bookmark}
  \urlstyle{same} % normal text font (alternatives: tt, rm, sf)
}{}
""",
titledata='')

head = head_template.substitute(parts)

head_table = head_template.substitute(
    dict(parts, requirements=parts['requirements'] + parts['longtable']))

head_booktabs = head_template.substitute(
    dict(parts, requirements=parts['requirements']
         + '\\usepackage{booktabs}\n' + parts['longtable']))

head_textcomp = head_template.substitute(
    dict(parts, requirements=parts['requirements']
         + '\\usepackage{textcomp} % text symbol macros\n'))

head_alltt = head_template.substitute(
    dict(parts, requirements=parts['requirements']
         + '\\usepackage{alltt}\n'))


samples_default = {}
samples_docutils_toc = {}
samples_book = {}
samples_latex_sectnum = {}
samples_latex_citations = {}
samples_stylesheet = {}
samples_stylesheet_embed = {}
samples_table_style_auto = {}
samples_table_style_booktabs = {}
samples_bibtex = {}

samples_default['url_chars'] = [
["http://nowhere/url_with%28parens%29",
head + r"""
\url{http://nowhere/url_with\%28parens\%29}

\end{document}
"""],
]

samples_default['textcomp'] = [
["2 µm is just 2/1000000 m",
head_textcomp + r"""
2 µm is just 2/1000000 m

\end{document}
"""],
]

samples_default['spanish_quote'] = [
[".. role:: language-es\n\nUnd damit :language-es:`basta`!",
head_template.substitute(dict(parts,
requirements=r"""\usepackage{ifthen}
\usepackage[T1]{fontenc}
\usepackage[spanish,english]{babel}
\AtBeginDocument{\shorthandoff{.<>}}
""")) + r"""
Und damit \foreignlanguage{spanish}{basta}!

\end{document}
"""],
]

samples_default['code_role'] = [
[':code:`x=1`',
head_template.substitute(dict(parts, requirements=parts['requirements']
                              + '\\usepackage{color}\n',
                              fallbacks=parts['fallbacks_highlight']))
+ r"""
\texttt{\DUrole{code}{x=1}}

\end{document}
"""],
]

samples_docutils_toc['table_of_contents'] = [
["""\
.. contents:: Table of Contents

Title 1
=======
Paragraph 1.

Title 2
-------
Paragraph 2.
""",
# expected output
head_template.substitute(dict(parts,
    requirements=parts['requirements'] + '\\setcounter{secnumdepth}{0}\n',
    fallbacks=r"""
% class handling for environments (block-level elements)
% \begin{DUclass}{spam} tries \DUCLASSspam and
% \end{DUclass}{spam} tries \endDUCLASSspam
\ifx\DUclass\undefined % poor man's "provideenvironment"
 \newenvironment{DUclass}[1]%
  {% "#1" does not work in end-part of environment.
   \def\DocutilsClassFunctionName{DUCLASS#1}
     \csname \DocutilsClassFunctionName \endcsname}%
  {\csname end\DocutilsClassFunctionName \endcsname}%
\fi

% title for topics, admonitions, unsupported section levels, and sidebar
\providecommand*{\DUtitle}[1]{%
  \smallskip\noindent\textbf{#1}\smallskip}

\providecommand*{\DUCLASScontents}{%
  \renewenvironment{itemize}%
    {\begin{list}{}{\setlength{\partopsep}{0pt}
                    \setlength{\parsep}{0pt}}
                   }%
    {\end{list}}%
}
""")) + r"""
\phantomsection\label{table-of-contents}
\pdfbookmark[1]{Table of Contents}{table-of-contents}

\begin{DUclass}{contents}

\DUtitle{Table of Contents}

\begin{itemize}
\item \hyperref[title-1]{Title 1}

\begin{itemize}
\item \hyperref[title-2]{Title 2}
\end{itemize}
\end{itemize}
\end{DUclass}


\section{Title 1%
  \label{title-1}%
}

Paragraph 1.


\subsection{Title 2%
  \label{title-2}%
}

Paragraph 2.

\end{document}
"""],
]

samples_default['footnote_text'] = [
["""\
.. [1] paragraph

.. [2]

.. [3] 1. enumeration
""",
# expected output
head_template.substitute(dict(parts,
    fallbacks=r"""
% numerical or symbol footnotes with hyperlinks and backlinks
\providecommand*{\DUfootnotemark}[3]{%
  \raisebox{1em}{\hypertarget{#1}{}}%
  \hyperlink{#2}{\textsuperscript{#3}}%
}
\providecommand{\DUfootnotetext}[4]{%
  \begingroup%
  \renewcommand{\thefootnote}{%
    \protect\raisebox{1em}{\protect\hypertarget{#1}{}}%
    \protect\hyperlink{#2}{#3}}%
  \footnotetext{#4}%
  \endgroup%
}
""")) + r"""%
\DUfootnotetext{footnote-1}{footnote-1}{1}{%
paragraph
}
%
\DUfootnotetext{footnote-2}{footnote-2}{2}{}
%
\DUfootnotetext{footnote-3}{footnote-3}{3}{
\begin{enumerate}
\item enumeration
\end{enumerate}
}

\end{document}
"""],
]

samples_default['no_sectnum'] = [
["""\
.. contents::

first section
-------------
""",
# expected output
head_template.substitute(dict(parts,
    requirements=parts['requirements'] + '\\setcounter{secnumdepth}{0}\n'
)) + r"""
\phantomsection\label{contents}
\pdfbookmark[1]{Contents}{contents}
\tableofcontents


\section{first section%
  \label{first-section}%
}

\end{document}
"""],
]

samples_default['sectnum'] = [
["""\
.. contents::
.. sectnum::

first section
-------------
""",
# expected output
head_template.substitute(dict(parts,
    requirements=parts['requirements'] + '\\setcounter{secnumdepth}{0}\n'
)) + r"""
\phantomsection\label{contents}
\pdfbookmark[1]{Contents}{contents}
\tableofcontents


\section{1   first section%
  \label{first-section}%
}

\end{document}
"""],
]

samples_default['depth'] = [
["""\
.. contents::
    :depth: 1

first section
-------------
""",
# expected output
head_template.substitute(dict(parts,
    requirements=parts['requirements'] + '\\setcounter{secnumdepth}{0}\n'
)) + r"""
\phantomsection\label{contents}
\pdfbookmark[1]{Contents}{contents}
\setcounter{tocdepth}{1}
\tableofcontents


\section{first section%
  \label{first-section}%
}

\end{document}
"""],
]

samples_book['depth'] = [
["""\
.. contents::
    :depth: 1

first chapter
-------------
""",
# expected output
head_template.substitute(dict(parts,
    head_prefix=r"""\documentclass[a4paper]{book}
""",
    requirements=parts['requirements'] + '\\setcounter{secnumdepth}{0}\n'
)) + r"""
\phantomsection\label{contents}
\pdfbookmark[1]{Contents}{contents}
\setcounter{tocdepth}{0}
\tableofcontents


\chapter{first chapter%
  \label{first-chapter}%
}

\end{document}
"""],
]


samples_latex_sectnum['no_sectnum'] = [
["""\
some text

first section
-------------
""",
# expected output
head_template.substitute(dict(parts, requirements=parts['requirements']
                              + '\\setcounter{secnumdepth}{0}\n')) + r"""
some text


\section{first section%
  \label{first-section}%
}

\end{document}
"""],
]

samples_latex_sectnum['sectnum'] = [
["""\
.. sectnum::

some text

first section
-------------
""",
# expected output
head_template.substitute(dict(parts,
    requirements=parts['requirements'] + '\\setcounter{secnumdepth}{0}\n'
)) + r"""
some text


\section{first section%
  \label{first-section}%
}

\end{document}
"""],
]

samples_latex_citations['citations_with_underscore'] = [
["""\
Just a test citation [my_cite2006]_.

.. [my_cite2006]
   The underscore is mishandled.
""",
# expected output
head + r"""
Just a test citation \cite{my_cite2006}.

\begin{thebibliography}{my\_cite2006}
\bibitem[my\_cite2006]{my_cite2006}{
The underscore is mishandled.
}
\end{thebibliography}

\end{document}
"""],
]


samples_latex_citations['adjacent_citations'] = [
["""\
Two non-citations: [MeYou2007]_[YouMe2007]_.

Need to be separated for grouping: [MeYou2007]_ [YouMe2007]_.

Two spaces (or anything else) for no grouping: [MeYou2007]_  [YouMe2007]_.

But a line break should work: [MeYou2007]_
[YouMe2007]_.

.. [MeYou2007] not.
.. [YouMe2007] important.
""",
# expected output
head + r"""
Two non-citations: {[}MeYou2007{]}\_{[}YouMe2007{]}\_.

Need to be separated for grouping: \cite{MeYou2007,YouMe2007}.

Two spaces (or anything else) for no grouping: \cite{MeYou2007}  \cite{YouMe2007}.

But a line break should work: \cite{MeYou2007,YouMe2007}.

\begin{thebibliography}{MeYou2007}
\bibitem[MeYou2007]{MeYou2007}{
not.
}
\bibitem[YouMe2007]{YouMe2007}{
important.
}
\end{thebibliography}

\end{document}
"""],
]


samples_default['enumerated_lists'] = [
["""\
1. Item 1.
2. Second to the previous item this one will explain

  a) nothing.
  b) or some other.

3. Third is

  (I) having pre and postfixes
  (II) in roman numerals.
""",
# expected output
head + r"""
\begin{enumerate}
\item Item 1.

\item Second to the previous item this one will explain
\end{enumerate}

\begin{quote}
\begin{enumerate}
\renewcommand{\labelenumi}{\alph{enumi})}
\item nothing.

\item or some other.
\end{enumerate}
\end{quote}

\begin{enumerate}
\setcounter{enumi}{2}
\item Third is
\end{enumerate}

\begin{quote}
\begin{enumerate}
\renewcommand{\labelenumi}{(\Roman{enumi})}
\item having pre and postfixes

\item in roman numerals.
\end{enumerate}
\end{quote}

\end{document}
"""],
]

# TODO: need to test for quote replacing if the language uses "ASCII-quotes"
# as active character (e.g. de (ngerman)).


samples_default['table_caption'] = [
["""\
.. table:: Foo

   +-----+-----+
   |     |     |
   +-----+-----+
   |     |     |
   +-----+-----+
""",
head_table + r"""
\setlength{\DUtablewidth}{\linewidth}%
\begin{longtable}{|p{0.075\DUtablewidth}|p{0.075\DUtablewidth}|}
\caption{Foo}\\
\hline
 &  \\
\hline
 &  \\
\hline
\end{longtable}

\end{document}
"""],
]

samples_default['table_styles'] = [
["""\
.. table::
   :class: borderless

   +-----+-----+
   |  1  |  2  |
   +-----+-----+
   |  3  |  4  |
   +-----+-----+
""",
head_table + """
\\setlength{\\DUtablewidth}{\\linewidth}%
\\begin{longtable*}{p{0.075\\DUtablewidth}p{0.075\\DUtablewidth}}

1
 & \n\
2
 \\\\

3
 & \n\
4
 \\\\
\\end{longtable*}

\\end{document}
"""],
["""\
.. table::
   :class: booktabs

   +-----+-+
   |  1  |2|
   +-----+-+
""",
head_booktabs + """
\\setlength{\\DUtablewidth}{\\linewidth}%
\\begin{longtable*}{p{0.075\\DUtablewidth}p{0.028\\DUtablewidth}}
\\toprule

1
 & \n\
2
 \\\\
\\bottomrule
\\end{longtable*}

\\end{document}
"""],
["""\
.. table::
   :class: colwidths-auto

   +-----+-+
   |  1  |2|
   +-----+-+
""",
head_table + r"""
\begin{longtable*}{|l|l|}
\hline
1 & 2 \\
\hline
\end{longtable*}

\end{document}
"""],
["""\
.. table::
   :widths: auto

   +-----+-+
   |  1  |2|
   +-----+-+
""",
head_table + r"""
\begin{longtable*}{|l|l|}
\hline
1 & 2 \\
\hline
\end{longtable*}

\end{document}
"""],
["""\
.. table::
   :widths: 15, 30

   +-----+-----+
   |  1  |  2  |
   +-----+-----+
""",
head_table + """
\\setlength{\\DUtablewidth}{\\linewidth}%
\\begin{longtable*}{|p{0.191\\DUtablewidth}|p{0.365\\DUtablewidth}|}
\\hline

1
 & \n\
2
 \\\\
\\hline
\\end{longtable*}

\\end{document}
"""],
]

samples_table_style_booktabs['table_styles'] = [
# borderless overrides "booktabs" table_style
["""\
.. table::
   :class: borderless

   +-----+-----+
   |  1  |  2  |
   +-----+-----+
   |  3  |  4  |
   +-----+-----+
""",
head_table + """
\\setlength{\\DUtablewidth}{\\linewidth}%
\\begin{longtable*}{p{0.075\\DUtablewidth}p{0.075\\DUtablewidth}}

1
 & \n\
2
 \\\\

3
 & \n\
4
 \\\\
\\end{longtable*}

\\end{document}
"""],
["""\
.. table::
   :widths: auto

   +-----+-+
   |  1  |2|
   +-----+-+
""",
head_booktabs + r"""
\begin{longtable*}{ll}
\toprule
1 & 2 \\
\bottomrule
\end{longtable*}

\end{document}
"""],
["""\
.. table::
   :widths: 15, 30

   +-----+-----+
   |  1  |  2  |
   +-----+-----+
""",
head_booktabs + """
\\setlength{\\DUtablewidth}{\\linewidth}%
\\begin{longtable*}{p{0.191\\DUtablewidth}p{0.365\\DUtablewidth}}
\\toprule

1
 & \n\
2
 \\\\
\\bottomrule
\\end{longtable*}

\\end{document}
"""],
]
samples_table_style_auto['table_styles'] = [
["""\
.. table::
   :class: borderless

   +-----+-----+
   |  1  |  2  |
   +-----+-----+
   |  3  |  4  |
   +-----+-----+
""",
head_table + r"""
\begin{longtable*}{ll}
1 & 2 \\
3 & 4 \\
\end{longtable*}

\end{document}
"""],
["""\
.. table::
   :class: booktabs

   +-----+-+
   |  1  |2|
   +-----+-+
""",
head_booktabs + r"""
\begin{longtable*}{ll}
\toprule
1 & 2 \\
\bottomrule
\end{longtable*}

\end{document}
"""],
# given width overrides "colwidth-auto"
["""\
.. table::
   :widths: 15, 30

   +-----+-----+
   |  1  |  2  |
   +-----+-----+
""",
head_table + """
\\setlength{\\DUtablewidth}{\\linewidth}%
\\begin{longtable*}{|p{0.191\\DUtablewidth}|p{0.365\\DUtablewidth}|}
\\hline

1
 & \n\
2
 \\\\
\\hline
\\end{longtable*}

\\end{document}
"""],
]

samples_default['table_align'] = [
["""\
.. table::
   :align: right

   +-----+-----+
   |  1  |  2  |
   +-----+-----+
""",
head_table + """
\\setlength{\\DUtablewidth}{\\linewidth}%
\\begin{longtable*}[r]{|p{0.075\\DUtablewidth}|p{0.075\\DUtablewidth}|}
\\hline

1
 & \n\
2
 \\\\
\\hline
\\end{longtable*}

\\end{document}
"""],
]

samples_default['table_empty_cells'] = [
["""\
===== ======
Title
===== ======
entry value1
===== ======
""",
head_table + """
\\setlength{\\DUtablewidth}{\\linewidth}%
\\begin{longtable*}{|p{0.075\\DUtablewidth}|p{0.086\\DUtablewidth}|}
\\hline
\\textbf{%
Title
} &  \\\\
\\hline
\\endfirsthead
\\hline
\\textbf{%
Title
} &  \\\\
\\hline
\\endhead
\\multicolumn{2}{p{0.16\\DUtablewidth}}{\\raggedleft\\ldots continued on next page}\\\\
\\endfoot
\\endlastfoot

entry
 & \n\
value1
 \\\\
\\hline
\\end{longtable*}

\\end{document}
"""],
["""\
+----+----+
| c3 | c4 |
+----+----+
|         |
+---------+
""",
head_table + """
\\setlength{\\DUtablewidth}{\\linewidth}%
\\begin{longtable*}{|p{0.063\\DUtablewidth}|p{0.063\\DUtablewidth}|}
\\hline

c3
 & \n\
c4
 \\\\
\\hline
\\multicolumn{2}{|p{0.13\\DUtablewidth}|}{} \\\\
\\hline
\\end{longtable*}

\\end{document}
"""],
]

samples_default['table_nonstandard_class'] = [
["""\
.. table::
   :class: my-class

   +-----+-----+
   |  1  |  2  |
   +-----+-----+
   |  3  |  4  |
   +-----+-----+
""",
head_template.substitute(
    dict(
        parts,
        requirements=parts['requirements'] + parts['longtable'],
        fallbacks=r"""
% class handling for environments (block-level elements)
% \begin{DUclass}{spam} tries \DUCLASSspam and
% \end{DUclass}{spam} tries \endDUCLASSspam
\ifx\DUclass\undefined % poor man's "provideenvironment"
 \newenvironment{DUclass}[1]%
  {% "#1" does not work in end-part of environment.
   \def\DocutilsClassFunctionName{DUCLASS#1}
     \csname \DocutilsClassFunctionName \endcsname}%
  {\csname end\DocutilsClassFunctionName \endcsname}%
\fi
"""
    )
) + """
\\begin{DUclass}{my-class}
\\setlength{\\DUtablewidth}{\\linewidth}%
\\begin{longtable*}{|p{0.075\\DUtablewidth}|p{0.075\\DUtablewidth}|}
\\hline

1
 & \n\
2
 \\\\
\\hline

3
 & \n\
4
 \\\\
\\hline
\\end{longtable*}
\\end{DUclass}

\\end{document}
"""],
]

# The "[" needs to be protected (otherwise it will be seen as an
# option to "\\", "\item", etc. ).

samples_default['bracket_protection'] = [
["""
* [no option] to this item
""",
head + r"""
\begin{itemize}
\item {[}no option{]} to this item
\end{itemize}

\end{document}
"""],
]

samples_default['literal_block'] = [
["""\
Test special characters { [ \\\\ ] } in literal block::

  { [ ( \\macro

  } ] )
""",
head_alltt + r"""
Test special characters \{ {[} \textbackslash{} {]} \} in literal block:

\begin{quote}
\begin{alltt}
\{ [ ( \textbackslash{}macro

\} ] )
\end{alltt}
\end{quote}

\end{document}
"""],
]

samples_default['raw'] = [
[r""".. raw:: latex

   $E=mc^2$

A paragraph.

.. |sub| raw:: latex

   (some raw text)

Foo |sub|
same paragraph.
""",
head + r"""
$E=mc^2$

A paragraph.

Foo (some raw text)
same paragraph.

\end{document}
"""],
[r""".. compound::

  Compound paragraph

  .. raw:: LaTeX

     raw LaTeX block

  compound paragraph continuation.
""",
head_template.substitute(
    dict(parts,
         fallbacks=r"""
% class handling for environments (block-level elements)
% \begin{DUclass}{spam} tries \DUCLASSspam and
% \end{DUclass}{spam} tries \endDUCLASSspam
\ifx\DUclass\undefined % poor man's "provideenvironment"
 \newenvironment{DUclass}[1]%
  {% "#1" does not work in end-part of environment.
   \def\DocutilsClassFunctionName{DUCLASS#1}
     \csname \DocutilsClassFunctionName \endcsname}%
  {\csname end\DocutilsClassFunctionName \endcsname}%
\fi
""")
) + r"""
\begin{DUclass}{compound}
Compound paragraph
raw LaTeX block
compound paragraph continuation.
\end{DUclass}

\end{document}
"""],
]

samples_default['title_with_inline_markup'] = [
["""\
This is the *Title*
===================

This is the *Subtitle*
----------------------

This is a *section title*
~~~~~~~~~~~~~~~~~~~~~~~~~

This is the *document*.
""",
head_template.substitute(dict(parts,
    requirements=parts['requirements'] + '\\setcounter{secnumdepth}{0}\n',
    fallbacks=r"""
% subtitle (in document title)
\providecommand*{\DUdocumentsubtitle}[1]{{\large #1}}
""",
    pdfsetup=parts['pdfsetup'] + r"""\hypersetup{
  pdftitle={This is the Title},
}
""", titledata=r"""\title{This is the \emph{Title}%
  \label{this-is-the-title}%
  \\%
  \DUdocumentsubtitle{This is the \emph{Subtitle}}%
  \label{this-is-the-subtitle}}
\author{}
\date{}
""")) + r"""\maketitle


\section{This is a \emph{section title}%
  \label{this-is-a-section-title}%
}

This is the \emph{document}.

\end{document}
"""],
]

samples_stylesheet['two-styles'] = [
["""two stylesheet links in the header""",
head_template.substitute(dict(parts,
stylesheet=r"""\usepackage{%s}
\input{%s}
""" % (spam, ham))) + r"""
two stylesheet links in the header

\end{document}
"""],
]

samples_stylesheet_embed['two-styles'] = [
["""two stylesheets embedded in the header""",
head_template.substitute(dict(parts,
stylesheet=r"""% Cannot embed stylesheet:
%  [Errno 2] No such file or directory: '""" + spam + r""".sty'
% embedded stylesheet: """ + ham + r"""
\newcommand{\ham}{wonderful ham}

""")) + r"""
two stylesheets embedded in the header

\end{document}
"""],
]

samples_bibtex['alpha'] = [
["""\
Just a test citation [book-full]_.
""",
head + r"""
Just a test citation \cite{book-full}.

\bibliographystyle{alpha}
\bibliography{xampl}

\end{document}
"""],
["""\
No bibliography if there is no citation.
""",
head + r"""
No bibliography if there is no citation.

\end{document}
"""],
]


if __name__ == '__main__':
    unittest.main()
