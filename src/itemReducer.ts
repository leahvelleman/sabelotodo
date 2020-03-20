import {ListItem, Action} from './interfaces'
import { MOVE_ITEM } from './itemActions'

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
        default:
            return state;
    }
}

export default itemReducer;
