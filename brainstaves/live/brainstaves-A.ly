
\version "2.18.2"
% automatically converted by musicxml2ly from brainstaves-test-flight4.xml

\header {
    encodingsoftware = "MuseScore 2.1.0"
    encodingdate = "2019-04-23"
    % title = "Brainstaves"
    tagline = ""  % removed 
    }

#(set-global-staff-size 20.0750126457)
\paper {
    paper-width = 21.0\cm
    paper-height = 29.7\cm
    top-margin = 1.0\cm
    bottom-margin = 1.0\cm
    left-margin = 1.0\cm
    right-margin = 1.0\cm
    %paper-width = 29.7\cm
    %paper-height = 20.0\cm
    %top-margin = 0.5\cm
    %bottom-margin = 0.1\cm
    %left-margin = 0.5\cm
    %right-margin = 0.5\cm
    }
\layout {
    \context { \Score
        % autoBeaming = ##f
        }
    }
PartPOneVoiceOne =  {
    \clef "treble" \key c \major \numericTimeSignature\time 4/4 
%!!!v1
ais'16 cis''16 d''16 e''16 dis''16 cis''16 e''16 fis''16 dis''16 fis''16 f''16 dis''16 dis''16 f''16 g''16 dis''16 f''16 f''16 fis''16 fis''16 gis''16 fis''16 d''16 g''16 f''16 ais''16 c'''16 ais''16 c'''16 ais''16 g''16 gis''16 gis''16 ais''16 d'''16 b''16 b''16 g''16 g''16 ais''16 fis''16 g''16 a''16 b''16 a''16 gis''16 g''16 g''16 g''16 e''16 gis''16 gis''16 a''16 ais''16 b''16 d'''16 d'''16 cis'''16 d'''16 d'''16 c'''16 d'''16 c'''16 c'''16
    }

PartPTwoVoiceOne =  {
    \clef "treble" \key c \major \numericTimeSignature\time 4/4
%!!!v2
ais'16 ais'16 b'16 d''16 dis''16 d''16 d''16 c''16 cis''16 c''16 cis''16 b'16 ais'16 c''16 b'16 d''16 e''16 dis''16 dis''16 d''16 dis''16 fis''16 e''16 d''16 c''16 b'16 cis''16 cis''16 gis'16 g'16 g'16 f'16 e'16 f'16 f'16 dis'16 c'16 dis'16 dis'16 e'16 d'16 cis'16 d'16 c'16 ais16 ais16 ais16 b16 b16 a16 c'16 b16 cis'16 c'16 b16 c'16 b16 d'16 d'16 dis'16 f'16 e'16 f'16 f'16
    }

PartPThreeVoiceOne =  {
    \clef "alto" \key c \major \numericTimeSignature\time 4/4
%!!!va
dis'16 d'16 ais16 cis'16 cis'16 c'16 b16 c'16 d'16 f'16 g'16 fis'16 e'16 dis'16 cis'16 dis'16 e'16 d'16 d'16 b16 cis'16 b16 gis16 g16 e16 fis16 gis16 gis16 c'16 dis'16 e'16 e'16 f'16 fis'16 fis'16 fis'16 gis'16 a'16 g'16 dis'16 c'16 cis'16 dis'16 d'16 cis'16 b16 a16 a16 ais16 a16 g16 fis16 e16 dis16 f16 f16 f16 dis16 cis16 cis16 dis16 d16 c16 fis16
    }

PartPFourVoiceOne =  {
    \clef "bass" \key c \major \numericTimeSignature\time 4/4
%!!!vc
dis16 dis16 f16 e16 cis16 d16 d16 cis16 c16 a,16 ais,16 c16 dis16 cis16 dis16 cis16 f16 fis16 e16 cis16 cis16 c16 cis16 e16 e16 cis16 dis16 e16 dis16 f16 f16 e16 cis16 c16 a,16 gis,16 ais,16 f,16 c,16 e,16 d,16 cis,16 f,16 dis,16 dis,16 g,16 fis,16 fis,16 f,16 f,16 f,16 f,16 e,16 g,16 ais,16 a,16 a,16 ais,16 ais,16 c16 a,16 fis,16 fis,16 a,16
    }


% The score definition
\score {
    <<
        \new StaffGroup <<
            \new Staff <<
                \set Staff.instrumentName = "V1"
                \context Staff << 
                    \context Voice = "PartPOneVoiceOne" { \PartPOneVoiceOne }
                    >>
                >>
            \new Staff <<
                \set Staff.instrumentName = "V2"
                \context Staff << 
                    \context Voice = "PartPTwoVoiceOne" { \PartPTwoVoiceOne }
                    >>
                >>
            \new Staff <<
                \set Staff.instrumentName = "Va"
                \context Staff << 
                    \context Voice = "PartPThreeVoiceOne" { \PartPThreeVoiceOne }
                    >>
                >>
            \new Staff <<
                \set Staff.instrumentName = "Vc"
                \context Staff << 
                    \context Voice = "PartPFourVoiceOne" { \PartPFourVoiceOne }
                    >>
                >>
            
            >>
        
        >>
    \layout {}
    % To create MIDI output, uncomment the following line:
    \midi {}
    }

