/**
 * File: DecisionPanel.int.test.jsx
 * Author: Eric Morse
 * Date: May 11th, 2025
 *
 * Description:
 *   Integration test for the DecisionsPanel component in the AI Meeting Summarizer frontend.
 *   This test verifies that the DecisionsPanel renders decisions provided via props.
 *   Uses React Testing Library for rendering and assertion.
 */
import { render, screen } from '@testing-library/react';
import DecisionsPanel from '../../components/DecisionsPanel';

describe('DecisionsPanel (Integration)', () => {
    /**
     * Test: renders decisions from real data
     * Description:
     *   Renders the DecisionsPanel component with two sample decisions.
     *   Asserts that both decision texts are present in the document.
     *   Timeout is set to 20 seconds to allow for future expansion.
     */
    it('renders decisions from real data', () => {
        render(<DecisionsPanel decisions={['Decision 1', 'Decision 2']} />);
        expect(screen.getByText('Decision 1')).toBeInTheDocument();
        expect(screen.getByText('Decision 2')).toBeInTheDocument();
    }, 20000);
});
