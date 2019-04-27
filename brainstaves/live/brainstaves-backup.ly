
\version "2.18.2"
% automatically converted by musicxml2ly from brainstaves-test-flight4.xml

\header {
    encodingsoftware = "MuseScore 2.1.0"
    encodingdate = "2019-04-23"
    % title = "Brainstaves"
    }

#(set-global-staff-size 20.0750126457)
\paper {
    paper-width = 29.7\cm
    paper-height = 20.0\cm
    top-margin = 0.5\cm
    bottom-margin = 0.1\cm
    left-margin = 0.5\cm
    right-margin = 0.5\cm
    }
\layout {
    \context { \Score
        autoBeaming = ##f
        }
    }
PartPOneVoiceOne =  {
    \clef "treble" \key c \major \numericTimeSignature\time 4/4 c'16 [
    f''16 g'''16 ] r16 [ gis'16 r16 d'8 ] f'16 [ g'16 f'16 c''16
    ] e'4 | % 2
    d'16 [ c'16 a16 a16 ] b16 [ g16 c'16 e'16 ] f'16 [ a'16 g'16 g'16 ]
    d'16 [ d'16 e'16 c'16 ] \break | % 3
    b16 [ g16 b16 g16 ] g16 [ c'16 c'16 g'16 ] b'16 [ a'16 f'16 d'16 ]
    a'16 [ a'16 g'16 g'16 ] | % 4
    e''16 [ e''16 f''16 g''16 ] f''16 [ c''16 c''16 b'16 ] c''16 [ e''16
    g''16 a''16 ] c'''16 [ a''16 f''16 g''16 ] \bar "|."
    }

PartPTwoVoiceOne =  {
    \clef "treble" \key c \major \numericTimeSignature\time 4/4 a'16 [
    g'16 g'16 b16 ] f'16 [ b16 g16 a16 ] d'16 [ b16 g16 a16 ] f'16 [ f'16
    d'16 e'16 ] | % 2
    d'16 [ d'16 g'16 e'16 ] e'16 [ c'16 b16 c'16 ] g16 [ g16 g16 b16 ]
    e'16 [ a16 a16 g16 ] \break | % 3
    f'16 [ g16 g16 g16 ] c'16 [ d'16 c'16 c'16 ] d'16 [ c'16 e'16 a16 ]
    e'16 [ a'16 a'16 b'16 ] | % 4
    b'16 [ g'16 g'16 c''16 ] a'16 [ g'16 g'16 a'16 ] d''16 [ c''16 d''16
    d''16 ] g'16 [ f'16 f'16 f'16 ] \bar "|."
    }

PartPThreeVoiceOne =  {
    \clef "alto" \key c \major \numericTimeSignature\time 4/4 d'16 [ a'16
    c''16 c''16 ] f'16 [ e'16 d'16 d'16 ] c'16 [ c'16 a16 f16 ] a16 [ c'16
    g'16 g'16 ] | % 2
    f'16 [ e'16 a16 d'16 ] a16 [ f16 e16 a16 ] b16 [ g16 e16 g16 ] f16 [
    d16 d16 f16 ] \break | % 3
    c'16 [ g16 f16 d16 ] c'16 [ g16 e16 g16 ] g16 [ c16 e16 d16 ] a16 [
    g16 f16 d16 ] | % 4
    d16 [ c'16 b16 d'16 ] f'16 [ a'16 d''16 g'16 ] e'16 [ g'16 c'16 a16
    ] d16 [ f16 b16 a16 ] \bar "|."
    }

PartPFourVoiceOne =  {
    \clef "bass" \key c \major \numericTimeSignature\time 4/4 d16 [ d16
    f16 c16 ] e16 [ d16 g,16 f,16 ] g,16 [ g,16 d,16 f,16 ] f,16 [ g,16
    g,16 d,16 ] | % 2
    e,16 [ d,16 g,16 b,16 ] b,16 [ g,16 g,16 g,16 ] d,16 [ c16 d16 a16 ]
    f16 [ c'16 g16 e16 ] \break | % 3
    f16 [ f16 a,16 f,16 ] g,16 [ e16 g16 g16 ] a16 [ f16 g16 d16 ] d16 [
    c16 e16 d16 ] | % 4
    g16 [ g16 a16 c'16 ] f16 [ f16 f16 d16 ] e16 [ a,16 c16 d16 ] d16 [
    c'16 d'16 d'16 ] \bar "|."
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

