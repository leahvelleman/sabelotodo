import React, {useReducer} from 'react';
import './App.scss';
import List from './List';
import {ListItem} from './interfaces';
import itemReducer from './itemReducer'
import { DndProvider } from 'react-dnd'
import Backend from 'react-dnd-html5-backend'
import DropTarget from './DropTarget'


const fakeLists = [
  {
    name: "todo",
    description: "a todo list",
    id: 0,
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
  {
      name: "another list",
      description: "grocery list",
      id: 3,
      parent: 0
  },
  {
      name: "yet more",
      description: "grocery list",
      id: 4,
      parent: 0
  },
  {
    name: "yet more2",
    description: "grocery list",
    id: 5,
    parent: 3
},
]

interface ListItemDict {
  [key: string]: ListItem[];
}



const processList = (items: ListItem[]):ListItem[] => {
  const finalList:ListItem[] = [];
  const childrenDict:ListItemDict = {};

  const processChildren = (item:ListItem) => {
    const parentString = item.id.toString()
    if(childrenDict[parentString]) {
      item.children = childrenDict[parentString]
      item.children.forEach(processChildren)
    }
  }

  items.forEach((item) => {
    const newItem = {...item}
    if(newItem.parent !== undefined) {
      const parentString = newItem.parent.toString()
      if(!childrenDict[parentString]) {
        childrenDict[parentString] = [newItem]
      } else {
        childrenDict[parentString].push(newItem)
      }
    } else {
      finalList.push(newItem)
    }
    finalList.forEach(processChildren)
  })
  return finalList;
}


function App() {
  const [state, dispatch] = useReducer(itemReducer, {items: fakeLists});
  const listsWithChildren = processList(state.items)

  return (
    <div className="App">
      <DndProvider backend={Backend}>
        {listsWithChildren.map((list:ListItem, i) => {
          return (<List myList={list} isChild={false} dispatch={dispatch} key={i}/>)
        })}
        <DropTarget dispatch={dispatch} />
      </DndProvider>
    </div>
  );
}

export default App;
