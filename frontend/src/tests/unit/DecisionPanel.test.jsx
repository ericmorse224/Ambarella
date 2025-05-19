import { render, screen } from '@testing-library/react';
import DecisionsPanel from '../../components/DecisionsPanel';

describe('DecisionsPanel', () => {
    test('renders decisions', () => {
        render(<DecisionsPanel decisions={['Decision 1', 'Decision 2']} />);
        expect(screen.getByText('Decision 1')).toBeInTheDocument();
        expect(screen.getByText('Decision 2')).toBeInTheDocument();
    });
    test('does not render if decisions are empty', () => {
        render(<DecisionsPanel decisions={[]} />);
        expect(screen.queryByText(/Decisions:/i)).not.toBeInTheDocument();
    });
});
