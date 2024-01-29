\subsection{Ablation Study}

\begin{table}[h]
\renewcommand{\arraystretch}{1.25}
\centering
\begin{tabular}{@{}ccccc@{}}
\toprule
Modules    & R-L  & C    & BertS & CLIP-S \\ \midrule
A2+A3+A4   & 18.5 & 26.2 & 39.9  & 0.612  \\
A1+A3+A4   & 12.3 & 18.7 & 35.3  & 0.311  \\
A1+A2+A4   & 19.5 & 28.9 & 38.1  & 0.434  \\
A1+A2+A3+B4 & 28.9 & 32.3 & 43.8  & 0.582  \\
\textbf{A1+A2+A3+A4} & \textbf{35.9} & \textbf{41.3} & \textbf{60.8} & \textbf{0.638} \\ \bottomrule
\end{tabular}
\caption{\textbf{Ablation study on impact of proposed modules.} A1 denotes Audio-aware Environmental Feature Enhancing Module, A2 denotes Actor-tracking-aware Story Linking Module, A3 denotes Movie Clip Contextual Alignment Module, A4 for LLaMA2-13b, B4 for LLaMA2-7b.}
\label{tab.2}
\end{table}

\noindent \textbf{Effect of the proposed modules.} In this part, we first study the influence of each proposed module and the employed LLM on the final Movie Audio Description (MAD) performance. We separately remove each module from our design and evaluate the resulting MAD on the MC-eval dataset (\cref{tab.2}). The results show that removing the Audio-aware Environmental Feature Enhancing Module has minimal impact on the CLIP-S metrics, which primarily assess the correlation between movie frame visuals and text. However, removing the Actor-tracking-aware Story Linking and Movie Clip Contextual Alignment Modules, both crucial for visual information acquisition, significantly decreases the CLIP-S metrics and enlarges the gap between model-generated captions and the Ground Truth (GT). Furthermore, the LLM size significantly influences the MAD quality, with the 13b model of LLaMA2 yielding more human-like captions than the 7b model, underscoring model complexity's impact.

\begin{figure}[!ht]
\begin{center}
\includegraphics[scale=0.55]{fig5.pdf} 
 \vspace{-0.1in}
\caption{Result visualization of Actor-tracking-aware Story Linking Module. We visualize the retrieval results on MC-eval dataset, with the incorrectly identified samples highlighted in red.}
\label{fig.5}
 \vspace{-0.2in}
\end{center} 
\end{figure}

\begin{table}[htbp]
\renewcommand{\arraystretch}{1.25}
\centering
\begin{tabular}{ccccc}
\hline
\multirow{2}{*}{Methods} & \multicolumn{2}{c}{MC-eval(ours)} & \multicolumn{2}{c}{MovieNet} \\ \cline{2-5} 
                          & mAP & R1  & mAP & R1 \\ \hline
RetinaFace\cite{c72}      & 32.4 & 42.8 & 35.2 & 44.9 \\
Abaw\cite{c73}            & 39.3 & 43.2 & 42.5 & 49.7 \\
BoT\cite{c74}             & 52.4 & 63.1 & 61.3 & 77.2 \\
LTReID\cite{c75}          & 55.8 & 62.9 & 61.7 & 78.8 \\
\textbf{Ours}& \textbf{69.5} & \textbf{76.8} & \textbf{72.3} & \textbf{88.6} \\ \hline
\end{tabular}
\caption{Ablation study on impact of Actor-tracking-aware Story Linking Module.}
\label{tab.3}
\end{table}



% \subsection{Character recognition module Evaluation}
\textbf{Effect of  Actor-tracking-aware Story Linking Module.} The effectiveness of our Actor-tracking-aware Story Linking Module hinges greatly on the precision of character recognition. To evaluate this, we compare our proposed method with two face detection algorithms and three Re-Identification (ReID) algorithms, widely used for accurately identifying main characters in movie datasets. The results are shown \cref{tab.3}.  Comparing our approach with these five existing methods, our character recognition technique proves to significantly enhance the performance. \cref{fig.5} illustrates some examples of our recognition results.


\textbf{Effect of Movie Clip Contextual Alignment Module.} The Movie Clip Contextual Alignment Module plays a pivotal role in our design, as it integrates visual information from preceding dialog-rich clips into the caption generation process for the current clip. To understand the influence of this module, we explore the qualitative relationship between the quality of the generated descriptions and the number of frames considered from previous clips involving character dialogue.  In this context, the quality of the Movie Audio Description is primarily evaluated using Bert S and CLIP-S metrics. The relationship between the number of prior frames considered and the resulting description quality, as measured by these metrics, is depicted in \cref{fig:fig6.}. We observe that as the number of prior subtitle-inclusive clips considered increases, the resulting movie audio description becomes more extensive. However, given the necessity to fit the narration within a specific time frame, a balance must be struck. When more than 96 frames are considered, the captions must be controlled for word count, leading to a more concise description. Consequently, this streamlining may result in a compromise in description quality.
