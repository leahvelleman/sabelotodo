import React from 'react';
import { render } from '@testing-library/react';
import List from './List';

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

test('test renders a list', () => {
  const { getByText } = render(<List myList={fakeList} isChild={false} />);
  const linkElement = getByText(fakeList.name);
  expect(linkElement).toBeInTheDocument();
});

test('test renders children', () => {
    const { getByText } = render(<List myList={fakeList} isChild={false} />);
    const linkElement = getByText(fakeList.children[0].name);
    expect(linkElement).toBeInTheDocument();
  });