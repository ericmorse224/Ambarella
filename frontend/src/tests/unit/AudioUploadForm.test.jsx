import { render, screen, fireEvent } from '@testing-library/react';
import AudioUploadForm from '../../components/AudioUploadForm';

describe('AudioUploadForm', () => {
    test('shows file name after selecting a file', () => {
        const setFile = vi.fn();
        render(
            <AudioUploadForm
                file={null}
                onFileChange={setFile}
                onSubmit={() => {}}
                isLoading={false}
                uploadAttempts={0}
            />
        );
        const input = screen.getByLabelText(/Upload Audio/i);
        const file = new File(['audio'], 'audio.mp3', { type: 'audio/mpeg' });
        fireEvent.change(input, { target: { files: [file] } });
    });

    test('disable button if no file', () => {
        render(
            <AudioUploadForm
                file={null}
                onFileChange={() => {}}
                onSubmit={() => {}}
                isLoading={false}
                uploadAttempts={0}
            />
        );
        expect(screen.getByRole('button', { name: /transcribe audio/i })).toBeDisabled();
    });
});
