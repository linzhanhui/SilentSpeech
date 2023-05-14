function [data_filtered] = pca_filter(data, n_channels)
% filter the input spatial data using PCA
% perform svd on the data
[U,S,V] = svd(data,'econ');
% non-normalized waveform
A = U*S;
% plot waveform if true
if false
    for i=1:n_channels
        figure(1);
        set(figure(1), 'Color', 'white');
        plot(t, A(:,i), 'LineWidth', 1, 'Color', [0.0118, 0.0359, 0.4824], 'DisplayName', ' component '+string(i));
        grid on
        xlabel('Time(s)', 'FontSize',14);
        xlim([min(t), max(t)]);
        ylabel('Non-normalized amplitude','FontSize',14);
        ylim([-0.6, 0.6]);
        legend('FontSize',14, 'box', 'off');
        title('Non-normalized waveform for component '+string(i));
        drawnow
        pause(1);
    end
end
% set the cols corresponding to omit_ind and the highest eigenvalue to zero in V
omit_ind = 6:n_channels;
V_reconstructed = V;
V_reconstructed(:, omit_ind) = 0;
V_reconstructed(:,1) = 0;
% reconstruct the original signal
data_filtered = A * V_reconstructed';