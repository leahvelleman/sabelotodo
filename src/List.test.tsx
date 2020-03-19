import React from 'react';
import { render, cleanup } from '@testing-library/react';
import List from './List';
import { DndProvider } from 'react-dnd'
import Backend from 'react-dnd-html5-backend';

const fakeList = {
    name: "todo",
    description: "a todo list",
    id: 0,
    children: [ 
        {
            name: "another list",
            description: "grocery list",
            id: 3,
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

test('test renders children', () => {
    const { getByText } = render(<FakeProvider><List myList={fakeList} isChild={false} dispatch={() => {}}/></FakeProvider>);
    const linkElement = getByText(fakeList.children[0].name);
    expect(linkElement).toBeInTheDocument();
});