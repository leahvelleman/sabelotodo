import React from 'react';
import { render, cleanup } from '@testing-library/react';
import List from './List';
import { DndProvider } from 'react-dnd'
import Backend from 'react-dnd-html5-backend';

const fakeList = {
    name: "todo",
    description: "a todo list",
    id: 0,
    done: false,
    children: [ 
        {
            name: "another list",
            description: "grocery list",
            id: 3,
            done: true,
        }
    ]
}

// @ts-ignore
const FakeProvider = ({children}) => {
    return <DndProvider backend={Backend}>{children}</DndProvider>
}

test('test renders a list', () => {
  const { getByText } = render(<FakeProvider><List myList={fakeList} isChild={false} dispatch={() => {}}/></FakeProvider>);
  const linkElement = getByText(fakeList.name);
  expect(linkElement).toBeInTheDocument();
});

test('test does not render children by default', () => {
    const { queryByText } = render(<FakeProvider><List myList={fakeList} isChild={false} dispatch={() => {}}/></FakeProvider>);
    const linkElement = queryByText(fakeList.children[0].name);
    expect(linkElement).toBeNull();
});

test('test renders children when expanded', () => {
    const { getByText, getByTestId } = render(<FakeProvider><List myList={fakeList} isChild={false} dispatch={() => {}}/></FakeProvider>);
    const expandButton = getByTestId('list-expanded');
    expandButton.click()
    const linkElement = getByText(fakeList.children[0].name);
    expect(linkElement).toBeInTheDocument();
});