import React, {useReducer} from 'react';
import { render, fireEvent } from '@testing-library/react';
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
  const { getByText } = render(<FakeProvider><List myList={fakeList} isChild={false} dispatch={() => {}} parentIds={[]}/></FakeProvider>);
  const linkElement = getByText(fakeList.name);
  expect(linkElement).toBeInTheDocument();
});

test('test does not render children by default', () => {
    const { queryByText } = render(<FakeProvider><List myList={fakeList} isChild={false} dispatch={() => {}} parentIds={[]}/></FakeProvider>);
    const linkElement = queryByText(fakeList.children[0].name);
    expect(linkElement).toBeNull();
});

test('test renders children when expanded', () => {
    const { getByText, getByTestId } = render(<FakeProvider><List myList={{...fakeList, expanded: true}} isChild={false} dispatch={() => {}} parentIds={[]}/></FakeProvider>);
    const linkElement = getByText(fakeList.children[0].name);
    expect(linkElement).toBeInTheDocument();
});

test('checkbox is checked if item is done', () => {
    // @ts-ignore
    const testItem = {...fakeList, done: true}
    const listId = testItem.id;
    const { getByTestId } = render(<FakeProvider><List myList={testItem} isChild={false} dispatch={() => {}} parentIds={[]}/></FakeProvider>);
    const checkbox = getByTestId(`done-checkbox-${listId}`)
    expect(checkbox).toHaveAttribute('checked')
});

test('checkbox is not checked if item is not done', () => {
    // @ts-ignore
    const testItem = {...fakeList}
    const listId = testItem.id;
    const { getByTestId } = render(<FakeProvider><List myList={testItem} isChild={false} dispatch={() => {}} parentIds={[]}/></FakeProvider>);
    const checkbox = getByTestId(`done-checkbox-${listId}`)
    expect(checkbox).not.toHaveAttribute('checked')
});