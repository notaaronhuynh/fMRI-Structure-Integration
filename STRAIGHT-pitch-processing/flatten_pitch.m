%% Flatten Pitch of Speech Stimuli using STRAIGHT
% Norman-Haignere Lab
% PI: Dr. Samuel Norman-Haignere
% Author: Aaron Huynh 
% Last commit: 18 April 2024

slow = ["420", "450", "500", "630", "750", "900"];
fast = ["150", "210", "250", "300"];
story_slow = ["1"];
story_fast = ["16"];

for dur = slow
    for story = story_slow
        % Construct the directory path
        directory = sprintf('/Users/ahuynh2/Documents/Norman-Haignere/temporal-window-stimulus-generation-code/stimuli/%sms/Story%s/', dur, story);

        % Get a list of all files in the directory ending with 'clip.wav'
        target = sprintf('Story%s_%sms.wav', story, dur);
        files = dir(fullfile(directory, target));

        % Iterate over each file in the directory
        for i = 1:numel(files)
            % Get the file name
            filename = fullfile(directory, files(i).name);

            % Call the function example_straight_f0setting.m for each file
            straight_f0setting(filename)
        end
    end
end


for dur = fast
    for story = story_fast
        % Construct the directory path
        directory = sprintf('/Users/ahuynh2/Documents/Norman-Haignere/temporal-window-stimulus-generation-code/stimuli/%sms/Story%s/', dur, story);
        
        % Get a list of all files in the directory ending with 'clip.wav'
        target = sprintf('Story%s_%sms.wav', story, dur);
        files = dir(fullfile(directory, target));
        
        % Iterate over each file in the directory
        for i = 1:numel(files)
            % Get the file name
            filename = fullfile(directory, files(i).name);
            
            % Call the function example_straight_f0setting.m for each file
            straight_f0setting(filename)
        end
    end
end
