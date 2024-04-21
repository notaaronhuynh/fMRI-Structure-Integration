function [sh sb shb syn_Harm] = straight_synthesis(sourceStructure, filterStructure, harmonic_jitter)
% si_str, si_sh, sh_shu, sh_shd, su
% stretch_factor,shift_factor,harm_shift_up_factor,harm_shift_down_factor,
% if nargin < 3
%     bias = 0.1;
% end

%%

testSubstrate.samplingFrequency = sourceStructure.samplingFrequency;
testSubstrate.sigmoidParameter = sourceStructure.sigmoidParameter;
testSubstrate.vuv = sourceStructure.vuv;
testSubstrate.f0 = sourceStructure.f0;
testSubstrate.temporalPositions = sourceStructure.temporalPositions;
testSubstrate.cutOffListFix = sourceStructure.cutOffListFix;
testSubstrate.targetF0 = sourceStructure.targetF0;
testSubstrate.exponent = sourceStructure.exponent;
testSubstrate.spectrogramSTRAIGHT = filterStructure.spectrogramSTRAIGHT;

testSubstrate.transitionWidth = 0.15;
testSubstrate.sourceOption = (1-0.5*sourceStructure.vuv');

%syn_Normal = generalSTRAIGHTsynthesisFrameworkR2(@interpFetcherFixRate, ...
%    @minimumPhaseResponse,@f0AdaptiveDClessPulseR2,@noiseBurstInFrequencyR2, ...
%    @generateBaseShifterSigmoid,testSubstrate);

option.deterministicHandleOption.biasFactor = harmonic_jitter;
option.feedingHandleOption.frameRateInSecond = 0.005;
option.deterministicHandleOption.sourceType = 'cosPlusBias';

% Regular resynthesis
syn_Harm = generalSTRAIGHTsynthesisFrameworkR2(@interpFetcherFixRate, ...
    @minimumPhaseResponse,@deterministicExcitationR2,@noiseBurstInFrequencyR2, ...
    @doNothingShifter,testSubstrate,option);

sh = syn_Harm.voicedOut;
sb = syn_Harm.unvoicedOut;
shb = syn_Harm.synthesisOut;
% fprintf('Done\n'); drawnow;

% % Noise part only
% syn_Noise = generalSTRAIGHTsynthesisFrameworkR2(@interpFetcherFixRate, ...
%     @minimumPhaseResponse,@noiseBurstInFrequencyWhisper,@noiseBurstInFrequencyR2, ...
%     @doNothingShifter,testSubstrate,option);

% Inharmonic - jittered
% option.deterministicHandleOption.biasFactor = jitter_amts;
% syn_Inharm_jitt = generalSTRAIGHTsynthesisFrameworkR2(@interpFetcherFixRate, ...
%     @minimumPhaseResponse,@deterministicExcitationR2,@noiseBurstInFrequencyR2, ...
%     @doNothingShifter,testSubstrate,option);

% % Inharmonic - stretched
% if length(stretch_factor)==1
%     harm_nums = 1:15;
%     stretch_factors = harm_nums.*(harm_nums-1)*stretch_factor;
%     option.deterministicHandleOption.biasFactor = stretch_factors;
% else
%     option.deterministicHandleOption.biasFactor = stretch_factor;
% end
% syn_Inharm_stretch = generalSTRAIGHTsynthesisFrameworkR2(@interpFetcherFixRate, ...
%     @minimumPhaseResponse,@deterministicExcitationR2,@noiseBurstInFrequencyR2, ...
%     @doNothingShifter,testSubstrate,option);

% % Inharmonic - shifted
% if length(shift_factor)==1
%     harm_nums = 1:15;
%     shift_factors = ones(size(harm_nums))*shift_factor;
%     option.deterministicHandleOption.biasFactor = shift_factors;
% else
%     option.deterministicHandleOption.biasFactor = shift_factor;
% end
% syn_Inharm_shift = generalSTRAIGHTsynthesisFrameworkR2(@interpFetcherFixRate, ...
%     @minimumPhaseResponse,@deterministicExcitationR2,@noiseBurstInFrequencyR2, ...
%     @doNothingShifter,testSubstrate,option);

% % Harmonic - pitch shifted up
% if length(harm_shift_up_factor)==1
%     harm_nums = 1:60;
%     shift_factors = harm_nums*harm_shift_up_factor;
%     option.deterministicHandleOption.biasFactor = shift_factors;
% else
%     harm_nums = 1:60;
%     shift_factors = harm_nums*harm_shift_up_factor(1);
%     option.deterministicHandleOption.biasFactor = shift_factors;
% end
% syn_Harm_shift_up = generalSTRAIGHTsynthesisFrameworkR2(@interpFetcherFixRate, ...
%     @minimumPhaseResponse,@deterministicExcitationR2,@noiseBurstInFrequencyR2, ...
%     @doNothingShifter,testSubstrate,option);
% 
% % Harmonic - pitch shifted down
% if length(harm_shift_down_factor)==1
%     harm_nums = 1:60;
%     shift_factors = harm_nums*harm_shift_down_factor;
%     option.deterministicHandleOption.biasFactor = shift_factors;
% else
%     harm_nums = 1:60;
%     shift_factors = harm_nums*harm_shift_down_factor(1);
%     option.deterministicHandleOption.biasFactor = shift_factors;
% end
% syn_Harm_shift_down = generalSTRAIGHTsynthesisFrameworkR2(@interpFetcherFixRate, ...
%     @minimumPhaseResponse,@deterministicExcitationR2,@noiseBurstInFrequencyR2, ...
%     @doNothingShifter,testSubstrate,option);
%%
 
%  if plot_sg
%      sg_Harm = stftSpectrogramStructure(syn_Harm.synthesisOut,fs,80,1,'nuttallwin12');
%      sg_Noise = stftSpectrogramStructure(syn_Noise.synthesisOut,fs,80,1,'nuttallwin12');
%      sg_Inharm = stftSpectrogramStructure(syn_Inharm.synthesisOut,fs,80,1,'nuttallwin12');
%      
%      %figure;
%      subplot(311);
%      imagesc([0 sg_Harm.temporalPositions(end)],[0 fs/2],max(-90,sg_Harm.dBspectrogram));
%      axis([0 sg_Harm.temporalPositions(end) 0 1000]);
%      title('Harmonic synthesis');
%      axis('xy');colorbar; grid
%      
%      subplot(312);
%      imagesc([0 sg_Noise.temporalPositions(end)],[0 fs/2],max(-90,sg_Noise.dBspectrogram));
%      axis([0 sg_Noise.temporalPositions(end) 0 1000]);
%      title('Noise only');
%      axis('xy');colorbar; grid
%      
%      subplot(313);
%      imagesc([0 sg_Inharm.temporalPositions(end)],[0 fs/2],max(-90,sg_Inharm.dBspectrogram));
%      axis([0 sg_Inharm.temporalPositions(end) 0 1000]);
%      title(['Inharm biasFactor = ',num2str(option.deterministicHandleOption.biasFactor)]);
%      axis('xy');colorbar; grid
%  end

%%

% si_jitt = syn_Inharm_jitt.voicedOut;
% si_str = syn_Inharm_stretch.voicedOut;
% si_sh = syn_Inharm_shift.voicedOut;
% sh_shu = syn_Harm_shift_up.voicedOut;
% sh_shd = syn_Harm_shift_down.voicedOut;
% su = syn_Noise.voicedOut;
