function IG_EEG_proc(pathname,filename)
% Processing for Ivan Gerov's FYP EEG using FieldTrip (2019-2020)
% INPUT:  pathname e.g. ='C:\Users\zumerj\Documents\FYP\2019_2020\Ivan\par_1_new'
%         filename e.g. ='lofi_new.fif'
%
% Download FieldTrip: either here http://www.fieldtriptoolbox.org/download
% or Github:  http://www.fieldtriptoolbox.org/development/git

% Add this fieldtrip folder now to your Matlab path
addpath('C:\Users\zumerj\Documents\MATLAB\fieldtrip') % Edit to be path on your computer
% Run ft_defaults which sets up all sorts of defaults and path definitions
ft_defaults

% Change this to be path
cd(pathname)
cfg=[];
cfg.dataset=filename;
eeg=ft_preprocessing(cfg);

trial_rcue(1:length(eeg.trial))=0;
trial_lcue(1:length(eeg.trial))=0;
trial_rtarg(1:length(eeg.trial))=0;
trial_ltarg(1:length(eeg.trial))=0;
for tt=1:length(eeg.trial)
  if isempty(find(diff(eeg.trial{tt}(3,:))==1)) && ~isempty(find(diff(eeg.trial{tt}(3,:))==2))
    trial_rcue(tt)=1;
  elseif isempty(find(diff(eeg.trial{tt}(3,:))==2)) && ~isempty(find(diff(eeg.trial{tt}(3,:))==1))
    trial_lcue(tt)=1;
  end
  if isempty(find(diff(eeg.trial{tt}(3,:))==3)) && ~isempty(find(diff(eeg.trial{tt}(3,:))==4))
    trial_rtarg(tt)=1;
  elseif isempty(find(diff(eeg.trial{tt}(3,:))==4)) && ~isempty(find(diff(eeg.trial{tt}(3,:))==3))
    trial_ltarg(tt)=1;
  end
end

%  Artifact rejection
cfg=[];
cfg.method='summary';
cfg.channel={'PO3' 'PO4'};
eeg_rej = ft_rejectvisual(cfg, eeg);  % variance under 650

[aa,bb,cc]=fileparts(filename);
save([bb '_data_rejected.mat'],'eeg_rej')

% If you wish to pick up from here
% load([bb '_data_rejected.mat'])

cfg=[];
cfg.lpfilter='yes';
cfg.lpfreq=25;
filt_eeg=ft_preprocessing(cfg,eeg_rej);

cueR_targR=sum([trial_rcue; trial_rtarg])==2;
cueR_targL=sum([trial_rcue; trial_ltarg])==2;
cueL_targR=sum([trial_lcue; trial_rtarg])==2;
cueL_targL=sum([trial_lcue; trial_ltarg])==2;

cfg=[];
cfg.trials=cueR_targR;
data_cueR_targR=ft_selectdata(cfg,filt_eeg)
cfg.trials=cueR_targL;
data_cueR_targL=ft_selectdata(cfg,filt_eeg)
cfg.trials=cueL_targR;
data_cueL_targR=ft_selectdata(cfg,filt_eeg)
cfg.trials=cueL_targL;
data_cueL_targL=ft_selectdata(cfg,filt_eeg)



%%  Extract ERP P1 and N1.  Target starts at 1.2 s.
% PO3 is on the left (=label{1}); PO4 on the right (=label{2})

cfg=[];
cfg.latency=[1.2 1.6]; % The first 400 ms after target onset
tlock_cueL_targL=ft_timelockanalysis(cfg,data_cueL_targL);
tlock_cueL_targR=ft_timelockanalysis(cfg,data_cueL_targR);
tlock_cueR_targL=ft_timelockanalysis(cfg,data_cueR_targL);
tlock_cueR_targR=ft_timelockanalysis(cfg,data_cueR_targR);


% We need to know when exactly to look for P1 and N1.... somewhat data dependent

% figure;plot(tlock_cueL_targL.time,[tlock_cueL_targR.avg(1,:); tlock_cueR_targR.avg(1,:)]);



%% Filter and FFT to obtain alpha power

cfg=[];
cfg.latency=[.3 1.1];
cuetarg_cueL_targL=ft_selectdata(cfg,data_cueL_targL);
cuetarg_cueL_targR=ft_selectdata(cfg,data_cueL_targR);
cuetarg_cueR_targL=ft_selectdata(cfg,data_cueR_targL);
cuetarg_cueR_targR=ft_selectdata(cfg,data_cueR_targR);

cfg=[];
cuetarg_cueR=ft_appenddata(cfg,cuetarg_cueR_targL,cuetarg_cueR_targR);
cuetarg_cueL=ft_appenddata(cfg,cuetarg_cueL_targL,cuetarg_cueL_targR);

cfg=[];
cfg.method='mtmfft';
cfg.output='pow';
cfg.pad=2;
cfg.taper='hanning';
cfg.foilim=[8 13];
alpha_cueL=ft_freqanalysis(cfg,cuetarg_cueL);
alpha_cueR=ft_freqanalysis(cfg,cuetarg_cueR);

cfg=[];
cfg.avgoverfreq='yes';
alpha_avg_cueL=ft_selectdata(cfg,alpha_cueL);
alpha_avg_cueR=ft_selectdata(cfg,alpha_cueR);

% PO3 is on the left (=label{1}); PO4 on the right (=label{2})
alpha_contra  =mean([alpha_avg_cueL.powspctrm(2) alpha_avg_cueR.powspctrm(1)]);
alpha_ipsi    =mean([alpha_avg_cueL.powspctrm(1) alpha_avg_cueR.powspctrm(2)]);

save([bb '_alpha.mat'],'alpha*')
save([bb '_alpha_ascii.csv'],'alpha*','-ascii','-tabs')


