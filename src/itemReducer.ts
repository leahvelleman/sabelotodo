import {ListItem, Action} from './interfaces'
import { MOVE_ITEM, TOGGLE_DONE, SET_EXPANDED } from './itemActions'

type ItemState = ListItem[]

const itemReducer = (state:ItemState, action:Action): ItemState => {
    switch (action.type) {
        case MOVE_ITEM:
            return state.map((item:ListItem) => {
                    if(item.id === action.draggedId) {
                        return {...item, parent: action.droppedId}
                    }
                    return item;
                })
        case TOGGLE_DONE:
            return state.map((item:ListItem) => {
                if(item.id === action.id) {
                    return {...item, done: !item.done}
                }
                return item;
            })
        case SET_EXPANDED:
            return state.map((item:ListItem) => {
                if(item.id === action.id) {
                    return {...item, expanded: action.expanded}
                }
                return item;
            })
        default:
            return state;
    }
}

export default itemReducer;
