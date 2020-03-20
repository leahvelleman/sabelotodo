import itemReducer from './itemReducer'
import {moveItemAction} from './itemActions'
import {ListItem} from './interfaces'


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
        const originalItem = fakeLists.find(findItem)
        const result = itemReducer(fakeLists, moveItemAction(itemId, parentId));
        const updatedItem = result.find(findItem)
        //@ts-ignore
        expect(updatedItem.parent).toEqual(parentId)
        expect(fakeLists.find(findItem)).toEqual(originalItem)
    });
})
