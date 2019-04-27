
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
r8 g'8 f'8 g'8 e'8 r8 a'8 r8 r8 c''8 c''8 r8 f''8 r8 r8 e''8 r8 c''8 r8 d''8 r8 f''8 r8 g''8 r8 a''8 r8 e''8 d''8 a'8 r8 a'8 a'8 c''8 r8 d'8 b8 a8 g8 r8 d'8 b8 c'8 a8 a8 r8 r8 r8 a8 c'8 r8 r8 d'8 g'8 a'8 b'8 c''8 a'8 r8 d''8 r8 b'8 d''8 b''8
    }

PartPTwoVoiceOne =  {
    \clef "treble" \key c \major \numericTimeSignature\time 4/4
%!!!v2
a'8 g'8 d'8 r8 r8 g'8 r8 e'8 f'8 r8 r8 c''8 f''8 r8 r8 r8 r8 r8 f'8 r8 r8 r8 r8 a'8 d''8 r8 f''8 e''8 d''8 r8 a''8 e''8 a'8 a'8 r8 a''8 r8 c''8 b'8 a'8 b8 r8 g'8 g'8 d'8 f'8 g'8 b'8 d'8 g'8 a'8 a'8 g'8 f'8 f'8 f'8 c'8 r8 b'8 c''8 a'8 e'8 e'8 c'8
    }

PartPThreeVoiceOne =  {
    \clef "alto" \key c \major \numericTimeSignature\time 4/4
%!!!va
dis'8 r8 g'8 r8 r8 b'8 g'8 r8 r8 r8 r8 a'8 r8 r8 f'8 b'8 r8 r8 c''8 r8 d'8 b8 cis'8 c'8 dis'8 r8 r8 r8 r8 r8 f''8 e''8 dis'8 c'8 cis'8 b8 d'8 b8 cis'8 b8 r8 b8 ais8 d'8 ais8 gis8 d'8 f8 fis8 r8 dis8 g8 e8 d8 fis8 dis8 dis8 d8 d8 r8 dis8 g8 c'8 a8
    }

PartPFourVoiceOne =  {
    \clef "bass" \key c \major \numericTimeSignature\time 4/4
%!!!vc
r8 r8 r8 r8 r8 r8 r8 r8 dis8 e8 r8 r8 r8 r8 f8 e8 e8 fis8 r8 fis8 cis8 r8 e8 b8 r8 ais,8 r8 r8 r8 r8 c8 c8 dis8 c8 gis,8 a,8 gis,8 r8 r8 d,8 cis,8 g,8 f,8 fis,8 r8 r8 e,8 dis,8 cis,8 e,8 r8 f8 e8 g8 gis8 fis8 ais8 f'8 c'8 e'8 r8 f'8 c'8 a8
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
    %  \midi {}
    }

