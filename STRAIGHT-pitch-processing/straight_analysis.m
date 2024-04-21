function [sourceStructure, filterStructure] = straight_analysis(wav,sr, varargin)

%% Analysis
fprintf('Straight analysis...\n');
r = exF0candidatesTSTRAIGHTGB(wav,sr);
rc = r;
rc = autoF0Tracking(r,wav);
rc.vuv = refineVoicingDecision(wav,rc);
% rc.vuv(:) = 1;
sourceStructure = aperiodicityRatioSigmoid(wav,rc,1,2,0);
filterStructure = exSpectrumTSTRAIGHTGB(wav,sr,sourceStructure);
t = sourceStructure.temporalPositions;

%% Optional Plotting

if ~optInputs(varargin, 'noplot')
    
    %%
    nfft = filterStructure.TANDEMSTRAIGHTconditions.FFTsize;
    nyq = (nfft/2)+1;
    f = (sr/2)*(0:nyq-1)/(nyq-1);

    figure;
    fontweight = 'Demi';
    fontsize = 14;
    set(gca,'FontWeight',fontweight,'FontSize',fontsize);
    imagesc(flipud(10*log10(filterStructure.spectrogramTANDEM)));
    set(gcf, 'PaperPosition', [0 0 12 8]);
    ytick = 1:50:length(f);
    set(gca,'YTick',ytick,'YTickLabel',round(f(end+1-ytick)),'FontWeight',fontweight,'FontSize',fontsize)
    ylabel('Frequency (Hz)');
    set(gca,'XTick',1:100:length(t),'XTickLabel',t(1:100:end),'FontWeight',fontweight,'FontSize',fontsize);
    xlabel('Time (sec)');
    title('Tandem Spectrogram');
    
    %%
    % draws lines
    if optInputs(varargin, 'lines')
        ln = varargin{optInputs(varargin, 'lines')+1};
        for i = 1:length(ln)
            [~,xi] = min(abs(ln(i)-t));
            hold on;
            plot([xi(1), xi(1)], [1, length(f)], 'k', 'LineWidth',1);
        end
    end
    
    % draws phoneme boundaries
    if optInputs(varargin, 'phones')
        set(gcf, 'Position', [0 0 1440 900]);
        phones = varargin{optInputs(varargin, 'phones')+1};
        onsets = varargin{optInputs(varargin, 'phones')+2};
        durations = varargin{optInputs(varargin, 'phones')+3};
        
        label_locations = nan(1,length(phones));
        for i = 1:length(phones)
            [~,xi] = min(abs(onsets(i)-t));
            hold on;
            plot([xi(1), xi(1)], [0, length(f)+1], 'k', 'LineWidth',1);
            [~,label_locations(i)] = min(abs(onsets(i)+durations(i)/2-t));
            
        end
        set(gca,'XTick',label_locations,'XTickLabel',phones,'FontSize',9);
        xlabel('Phonemes');
    end
    
end

