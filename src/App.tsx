import React, {useReducer} from 'react';
import logo from './logo.svg';
import './App.css';
import List from './List';
import {list} from './interfaces';
import itemReducer from './itemReducer'

const fakeLists = [
  {
    name: "todo",
    description: "a todo list",
    id: 0,
    children: [ {
      name: "another list",
      description: "grocery list",
      id: 3,
    },
    {
      name: "yet more",
      description: "grocery list",
      id: 4,
    },]
  },
  {
    name: "groceries",
    description: "grocery list",
    id: 1,
  },
  {
    name: "foo",
    id: 2,
  },
]


function App() {
  const [state, dispatch] = useReducer(itemReducer, {items: fakeLists});

  return (
    <div className="App">
      {state.items.map((list:list) => {
        return (<List myList={list} isChild={false}>
         
          </List>)
      })}
    </div>
  );
}

export default App;
