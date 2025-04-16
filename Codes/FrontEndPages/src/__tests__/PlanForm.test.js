import { render, screen, fireEvent } from '@testing-library/react';
import PlanForm from '../components/PlanForm';

test('renders plan generation form', () => {
  render(<PlanForm />);
  expect(screen.getByLabelText(/Student Level/i)).toBeInTheDocument();
  expect(screen.getByLabelText(/Duration/i)).toBeInTheDocument();
});

test('submits form with correct data', async () => {
  const mockSubmit = jest.fn();
  render(<PlanForm onSubmit={mockSubmit} />);
  
  fireEvent.change(screen.getByLabelText(/Student Level/i), {
    target: { value: 'beginner' },
  });
  
  fireEvent.click(screen.getByText(/Generate Plan/i));
  expect(mockSubmit).toHaveBeenCalled();
});