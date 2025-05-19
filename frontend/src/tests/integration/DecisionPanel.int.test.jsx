import { render, screen } from '@testing-library/react';
import DecisionsPanel from '../../components/DecisionsPanel';

describe('DecisionsPanel (Integration)', () => {
    it('renders decisions from real data', () => {
        render(<DecisionsPanel decisions={['Decision 1', 'Decision 2']} />);
        expect(screen.getByText('Decision 1')).toBeInTheDocument();
        expect(screen.getByText('Decision 2')).toBeInTheDocument();
    }, 20000);
});
