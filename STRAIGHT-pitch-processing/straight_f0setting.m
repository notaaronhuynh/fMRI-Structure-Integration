function straight_f0setting(audio_file)

    [wav, sr] = audioread(audio_file);
    [sourceStructure, filterStructure] = straight_analysis(wav, sr, 'noplot');
    sourceStructure_changed = sourceStructure;
    sourceStructure_changes.f0 = repmat(1, length(sourceStructure.f0), 100);    
    harmonic_jitter = 1; 
    [~, ~, shb, ~] = straight_synthesis(sourceStructure_changed, filterStructure, harmonic_jitter);

    [path, filename, ~] = fileparts(audio_file);
    
    outfile = fullfile(path, [filename '_flat.wav']);

    audiowrite(outfile, shb, sr);

end