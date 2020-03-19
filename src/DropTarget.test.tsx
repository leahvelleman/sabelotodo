import React from 'react';
import { render } from '@testing-library/react';
import DropTarget, {DroptargetTestId} from './DropTarget';
import { DndProvider } from 'react-dnd'
import Backend from 'react-dnd-html5-backend';

// @ts-ignore
const FakeProvider = ({children}) => {
    return <DndProvider backend={Backend}>{children}</DndProvider>
}

test('is hidden when no element is being dragged', () => {
  const { getByTestId } = render(<FakeProvider><DropTarget dispatch={() => {}}/></FakeProvider>);
  const dropBox = getByTestId(DroptargetTestId);
  expect(dropBox).toBeInTheDocument();
  expect(dropBox).toHaveClass('Drop-target')
  expect(dropBox).not.toHaveClass('Drop-target--hover')
  expect(dropBox).not.toHaveClass('Drop-target--dragging')
});
