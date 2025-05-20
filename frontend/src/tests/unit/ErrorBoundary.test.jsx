/**
 * File: ErrorBoundary.test.jsx
 * Author: Eric Morse
 * Date: May 11th, 2025
 * 
 * Description:
 * This test file verifies the functionality of the ErrorBoundary component.
 * It ensures that the ErrorBoundary correctly catches errors thrown by its child
 * components and displays the fallback UI with an appropriate error message.
 *
 * Test Cases:
 * - It renders the fallback UI ("Critical error") when a child component throws an error.
 */
import { render } from '@testing-library/react';
import ErrorBoundary from '../../components/ErrorBoundary';

/**
 * ProblemChild is a dummy React component that throws an error on render.
 * Used to simulate a component error inside ErrorBoundary.
 */
function ProblemChild() {
  throw new Error('Crash!');
}

it('displays fallback UI on error', () => {
  const { getByRole } = render(
    <ErrorBoundary>
      <ProblemChild />
    </ErrorBoundary>
  );
  expect(getByRole('alert')).toHaveTextContent(/critical error/i);
});
