import itemReducer from './itemReducer'
import {moveItemAction, toggleDoneAction} from './itemActions'
import {ListItem} from './interfaces'


const fakeLists = [
    {
      name: "todo",
      description: "a todo list",
      id: 0,
      done: false,
    },
    {
      name: "groceries",
      description: "grocery list",
      id: 1,
      done: false,
    },
    {
      name: "foo",
      id: 2,
      done: true,
    },
    {
        name: "another list",
        description: "grocery list",
        id: 3,
        parent: 0,
        done: false,
    },
    {
        name: "yet more",
        description: "grocery list",
        id: 4,
        parent: 0,
        done: true,
    },
  ]

const params = [
    {itemId: 3, parentId: 3},
    {itemId: 1, parentId: 2},
    {itemId: 2, parentId: 3},
    {itemId: 3, parentId: undefined},
    {itemId: 2, parentId: 1}
]

params.forEach(({itemId, parentId}) => {
    test('moves an item', () => {
        const findItem  = (item:ListItem):boolean => item.id === itemId;
        const originalItem = {...fakeLists.find(findItem)}
        const result = itemReducer(fakeLists, moveItemAction(itemId, parentId));
        const updatedItem = result.find(findItem)
        //@ts-ignore
        expect(updatedItem.parent).toEqual(parentId)
        // check that we're not modifying the original state
        expect(fakeLists.find(findItem)).toEqual(originalItem)
    });
})

test('toggles done', () => {
    const itemId = 2;
    const findItem  = (item:ListItem):boolean => item.id === itemId;
    const originalItem = {...fakeLists.find(findItem)}
    const result = itemReducer(fakeLists, toggleDoneAction(itemId));
    const updatedItem = result.find(findItem)
    //@ts-ignore
    expect(updatedItem.done).toEqual(!originalItem.done)
    expect(fakeLists.find(findItem)).toEqual(originalItem)
})
