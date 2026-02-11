from music21 import converter

def musicxml_to_chart(input_file, output_file):
    score = converter.parse(input_file)
    
    title = score.metadata.title or "Unknown"
    artist = score.metadata.composer or "Unknown"
    
    tempo_marks = score.flatten().getElementsByClass('MetronomeMark')
    bpm = tempo_marks[0].number if tempo_marks else 120
    
    print(f"Converting: {title} by {artist} at {bpm} BPM")
    
    # Build .chart file
    chart = f"""[Song]
{{
  Name = "{title}"
  Artist = "{artist}"
  Charter = "HeroChart"
  Offset = 0
  Resolution = 192
  Difficulty = 0
  Genre = "rock"
}}

[SyncTrack]
{{
  0 = TS 4
  0 = B {int(bpm * 1000)}
}}

[Events]
{{
}}

[ExpertSingle]
{{
"""
    
    # Get notes from first part
    notes = score.flatten().notes
    resolution = 192

    for note in notes:
        tick = int(note.offset * resolution)
        sustain = int(note.quarterLength * resolution)
        
        try:
            # Handle chords
            if note.isChord:
                for pitch in note.pitches:
                    button = pitch.midi % 5
                    chart += f"  {tick} = N {button} {sustain}\n"
            else:
                button = note.pitch.midi % 5
                chart += f"  {tick} = N {button} {sustain}\n"
        except:
            # Skip percussion or invalid notes
            continue
    
    chart += "}\n"
    
    # Write file
    with open(output_file, 'w') as f:
        f.write(chart)
    
    print(f"Created {output_file}!")

if __name__ == "__main__":
    musicxml_to_chart("Queen - Bohemian Rhapsody.mid", "notes.chart")