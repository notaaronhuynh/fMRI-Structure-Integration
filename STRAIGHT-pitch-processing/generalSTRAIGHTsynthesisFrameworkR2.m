function synthOutStructure = generalSTRAIGHTsynthesisFrameworkR2(...
    feedingHandle,responseHandle,deterministicHandle,randomHandle,shifterHandle,dataSubstrate,optionalParameters)
%   synthOutStructure = generalSTRAIGHTsynthesisFrameworkR2(...
%    feedingHandle,responseHandle,deterministicHandle,randomHandle,shifterHandle,dataSubstrate)

%   generalized synthesis routine for TANDEM-STRAIGHT manipulation
%   Designed and coded by Hideki Kawahara
%   21/Feb./2012
%   25/Feb./2012 first release
%   04/Mar./2012 more generalization
%   25/Mar./2012 further generalization

%startTime = tic;
synthOutStructure = [];
if isempty(feedingHandle)
    disp('input argument is empty!');
    return;
end;
if nargin == 7
    if isfield(optionalParameters,'deterministicHandleOption')
        deterministicHandleOption = optionalParameters.deterministicHandleOption;
    end;
    if isfield(optionalParameters,'randomHandleOption')
        randomHandleOption = optionalParameters.randomHandleOption;
    end;
    if isfield(optionalParameters,'feedingHandleOption')
        feedingHandleOption = optionalParameters.feedingHandleOption;
    end;
end;
%------------------------------------
fs = dataSubstrate.samplingFrequency;
if exist('feedingHandleOption','var')
    currentDataStructure = feedingHandle('initialize',dataSubstrate,[],feedingHandleOption);
else
    currentDataStructure = feedingHandle('initialize',dataSubstrate);
end;
eventLocations = currentDataStructure.eventLocations;
fftl = currentDataStructure.fftLength;
if exist('deterministicHandleOption','var')
    currentDataStructure = deterministicHandle('initialize',currentDataStructure,deterministicHandleOption);
else
    currentDataStructure = deterministicHandle('initialize',currentDataStructure);
end;
if exist('randomHandleOption','var')
    currentDataStructure = randomHandle('initialize',currentDataStructure,randomHandleOption);
else
    currentDataStructure = randomHandle('initialize',currentDataStructure);
end;
outBuffer = zeros(round(fs*eventLocations(end)),1);
outVoiced = zeros(round(fs*eventLocations(end)),1);
outUnvoiced = zeros(round(fs*eventLocations(end)),1);
%blankBuffer = zeros(fftl,1);
baseShifter = shifterHandle(dataSubstrate);
baseIndex = (1:fftl)'-fftl/2;
maxIndex = size(outBuffer,1);
voicedSpectrum = zeros(length(currentDataStructure.frequencyAxis),length(eventLocations));
unvoicedSpectrum = zeros(length(currentDataStructure.frequencyAxis),length(eventLocations));
voicedRMS = nan(length(eventLocations),1);
unvoicedRMS = nan(length(eventLocations),1);
for ii = 1:length(eventLocations)
    dataSubstrate.currentLocation = eventLocations(ii);
    currentDataStructure = feedingHandle('fetch',dataSubstrate,currentDataStructure);
    %sourceOption = currentDataStructure.sourceOption;
    currentIndex = floor(eventLocations(ii)*fs+1);
    fractionalIndex = eventLocations(ii)*fs+1-currentIndex;
    copyIndex = max(1,min(maxIndex,baseIndex+currentIndex));
    %f0 = currentDataStructure.f0;
    if currentDataStructure.vuv > 0.3
        randomCoeff = currentDataStructure.randomComponent;
        periodCoeff = sqrt(1-randomCoeff.^2);
        responseInFrequencyD = responseHandle(currentDataStructure.spectrum.*periodCoeff.^2);
        responseInFrequencyR = responseHandle(currentDataStructure.spectrum.*randomCoeff.^2);
        response = real(ifft(responseInFrequencyD.*deterministicHandle('fetch',currentDataStructure).*exp(-1i*baseShifter*fractionalIndex)));
        responseAP = real(ifft(responseInFrequencyR.*randomHandle('fetch',currentDataStructure)));
        outBuffer(copyIndex) = outBuffer(copyIndex)+response+responseAP;
        outVoiced(copyIndex) = outVoiced(copyIndex)+response;
        outUnvoiced(copyIndex) = outUnvoiced(copyIndex)+responseAP;
        voicedRMS(ii) = sqrt(mean(real(ifft(deterministicHandle('fetch',currentDataStructure).*exp(-1i*baseShifter*fractionalIndex))).^2));
        unvoicedRMS(ii) = sqrt(mean(real(ifft(randomHandle('fetch',currentDataStructure))).^2));
        voicedSpectrum(:,ii) = currentDataStructure.spectrum.*periodCoeff.^2;
        unvoicedSpectrum(:,ii) = currentDataStructure.spectrum.*randomCoeff.^2;
    else
        responseInFrequencyR = minimumPhaseResponse(currentDataStructure.spectrum);
        responseAP = real(ifft(responseInFrequencyR.*randomHandle('fetch',currentDataStructure)));%deterministicHandle('fetch',currentDataStructure).*exp(-1i*baseShifter*fractionalIndex)))
        outBuffer(copyIndex) = outBuffer(copyIndex)+responseAP;
        outUnvoiced(copyIndex) = outUnvoiced(copyIndex)+responseAP;
        unvoicedRMS(ii) = sqrt(mean(real(ifft(randomHandle('fetch',currentDataStructure))).^2));
        unvoicedSpectrum(:,ii) = currentDataStructure.spectrum;
    end;
end;
synthOutStructure.synthesisOut = outBuffer;
synthOutStructure.voicedOut = outVoiced;
synthOutStructure.unvoicedOut = outUnvoiced;
synthOutStructure.f = currentDataStructure.frequencyAxis;
synthOutStructure.voicedSpectrum = voicedSpectrum;
synthOutStructure.unvoicedSpectrum = unvoicedSpectrum;
synthOutStructure.voicedRMS = voicedRMS;
synthOutStructure.unvoicedRMS = unvoicedRMS;
synthOutStructure.t = eventLocations;
%synthOutStructure.elapsedTime = toc(startTime);
return;