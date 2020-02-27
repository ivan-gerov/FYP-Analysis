% Wrapper script for Ivan Gerov's FYP 2019-2020;
%
% Loops through all participants; extracts cue-related alpha power and
% target related ERP
%
% first determines optimal time for ERP from grand average, then goes back
% to extract it from each person

% Add this fieldtrip folder now to your Matlab path
addpath('C:\Users\zumerj\Documents\MATLAB\fieldtrip') % Edit to be path on your computer
% Run ft_defaults which sets up all sorts of defaults and path definitions
ft_defaults

addpath('C:\Users\zumerj\Documents\FYP\2019_2020\Ivan\code\')% change to where the code is stored

maindir='C:\Users\zumerj\Documents\FYP\2019_2020\Ivan\preprocessed\';
cd(maindir);

for parnum=1:11
  [alpha_contra(parnum,1),alpha_ipsi(parnum,1),tlock_silence{parnum}]=IG_EEG_processing([maindir 'par_' num2str(parnum) filesep 'blocks' filesep],'silence.fif',0);
  [alpha_contra(parnum,2),alpha_ipsi(parnum,2),tlock_white{parnum}]=IG_EEG_processing([maindir 'par_' num2str(parnum) filesep 'blocks' filesep],'white.fif',0);
  [alpha_contra(parnum,3),alpha_ipsi(parnum,3),tlock_lofi{parnum}]=IG_EEG_processing([maindir 'par_' num2str(parnum) filesep 'blocks' filesep],'lofi.fif',0);
end
save([maindir 'alpha_all.mat'],'alpha*')
save([maindir 'alpha_all_ascii.csv'],'alpha_contra','alpha_ipsi','-ascii','-tabs')

for parnum=1:11
  tlock_cueL_targL{parnum,1}=tlock_silence{parnum}.tlock_cueL_targL;
  tlock_cueR_targL{parnum,1}=tlock_silence{parnum}.tlock_cueR_targL;
  tlock_cueL_targR{parnum,1}=tlock_silence{parnum}.tlock_cueL_targR;
  tlock_cueR_targR{parnum,1}=tlock_silence{parnum}.tlock_cueR_targR;
  tlock_cueL_targL{parnum,2}=tlock_white{parnum}.tlock_cueL_targL;
  tlock_cueR_targL{parnum,2}=tlock_white{parnum}.tlock_cueR_targL;
  tlock_cueL_targR{parnum,2}=tlock_white{parnum}.tlock_cueL_targR;
  tlock_cueR_targR{parnum,2}=tlock_white{parnum}.tlock_cueR_targR;
  tlock_cueL_targL{parnum,3}=tlock_lofi{parnum}.tlock_cueL_targL;
  tlock_cueR_targL{parnum,3}=tlock_lofi{parnum}.tlock_cueR_targL;
  tlock_cueL_targR{parnum,3}=tlock_lofi{parnum}.tlock_cueL_targR;
  tlock_cueR_targR{parnum,3}=tlock_lofi{parnum}.tlock_cueR_targR;
end

cfg=[];
gravg_cueL_targL=ft_timelockgrandaverage(cfg,tlock_cueL_targL{:});
gravg_cueR_targR=ft_timelockgrandaverage(cfg,tlock_cueR_targR{:});
gravg_cueR_targL=ft_timelockgrandaverage(cfg,tlock_cueR_targL{:});
gravg_cueL_targR=ft_timelockgrandaverage(cfg,tlock_cueL_targR{:});
cfg.keepindividual='yes';
grind_cueL_targL=ft_timelockgrandaverage(cfg,tlock_cueL_targL{:});
grind_cueR_targR=ft_timelockgrandaverage(cfg,tlock_cueR_targR{:});
grind_cueR_targL=ft_timelockgrandaverage(cfg,tlock_cueR_targL{:});
grind_cueL_targR=ft_timelockgrandaverage(cfg,tlock_cueL_targR{:});

figure;plot(gravg_cueL_targL.time,gravg_cueL_targL.avg)
figure;plot(gravg_cueR_targR.time,gravg_cueR_targR.avg)
% PO3 is on the left (=label{1}); PO4 on the right (=label{2})
figure;plot(gravg_cueL_targL.time,[gravg_cueL_targL.avg(2,:); gravg_cueR_targL.avg(2,:) ])
figure;plot(gravg_cueL_targL.time,[gravg_cueR_targR.avg(1,:); gravg_cueL_targR.avg(1,:) ])
avg_peak_find=mean([gravg_cueL_targL.avg(2,:); gravg_cueR_targL.avg(2,:); gravg_cueR_targR.avg(1,:); gravg_cueL_targR.avg(1,:) ]);
[mx,mnd]=max(avg_peak_find);
gravg_cueL_targL.time(mnd)-1.2    % 176ms use for P peak; Perhaps this is P200 not P1?

targL_valid  =grind_cueL_targL.individual(:,2,mnd);
targL_invalid=grind_cueR_targL.individual(:,2,mnd);
targR_invalid=grind_cueL_targR.individual(:,1,mnd);
targR_valid  =grind_cueR_targR.individual(:,1,mnd);

save([maindir 'tlockall.mat'],'tlock*')
save([maindir 'targ_P.mat'],'targ*')
save([maindir 'targLV_P_ascii.csv'],'targL_valid','-ascii','-tabs')
save([maindir 'targRV_P_ascii.csv'],'targR_valid','-ascii','-tabs')
save([maindir 'targLI_P_ascii.csv'],'targL_invalid','-ascii','-tabs')
save([maindir 'targRI_P_ascii.csv'],'targR_invalid','-ascii','-tabs')


