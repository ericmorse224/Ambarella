/**
 * File: DecisionPanel.test.jsx
 * Author: Eric Morse
 * Date: May 11th, 2025
 * 
 * Description:
 * This file contains unit tests for the DecisionsPanel React component. 
 * The tests verify that the panel correctly renders decisions passed as props, 
 * and does not render the section if there are no decisions.
 * 
 * Usage:
 * - Run with Vitest/Jest or any compatible testing framework to validate 
 *   DecisionsPanel behavior.
 * 
 * Dependencies:
 * - @testing-library/react
 * - DecisionsPanel component (src/components/DecisionsPanel.jsx)
 */
import { render, screen } from '@testing-library/react';
import DecisionsPanel from '../../components/DecisionsPanel';

describe('DecisionsPanel', () => {
    /**
     * Test: renders decisions
     * Checks that the component displays each decision passed in the `decisions` prop.
     */
    test('renders decisions', () => {
        render(<DecisionsPanel decisions={['Decision 1', 'Decision 2']} />);
        expect(screen.getByText('Decision 1')).toBeInTheDocument();
        expect(screen.getByText('Decision 2')).toBeInTheDocument();
    });

    /**
     * Test: does not render if decisions are empty
     * Ensures the "Decisions:" heading is not present when an empty array is provided.
     */
    test('does not render if decisions are empty', () => {
        render(<DecisionsPanel decisions={[]} />);
        expect(screen.queryByText(/Decisions:/i)).not.toBeInTheDocument();
    });
});
