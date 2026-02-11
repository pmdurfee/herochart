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
    
    last_tick = -999
    min_gap = 64  # Space out notes more
    
    for note in notes:
        tick = int(note.offset * resolution)
        
        # Skip notes too close together
        if tick - last_tick < min_gap:
            continue
        
        last_tick = tick
        sustain = min(int(note.quarterLength * resolution), 288)  # Cap sustain
        
        try:
            # Handle chords - keep all notes
            if note.isChord:
                for pitch in note.pitches:
                    button = pitch.midi % 5
                    chart += f"  {tick} = N {button} {sustain}\n"
            else:
                button = note.pitch.midi % 5
                chart += f"  {tick} = N {button} {sustain}\n"
        except:
            continue
    
    chart += "}\n"
    
    # Write file
    with open(output_file, 'w') as f:
        f.write(chart)
    
    print(f"Created {output_file}!")

if __name__ == "__main__":
    musicxml_to_chart("Cavetown Juliet.mid", "notes.chart")