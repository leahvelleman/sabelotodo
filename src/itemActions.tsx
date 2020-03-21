import {Action} from './interfaces';

export const MOVE_ITEM = 'MOVE_ITEM';
export const moveItemAction = (draggedId:number, droppedId: number | undefined): Action => {
    return {
        type: MOVE_ITEM,
        draggedId,
        droppedId,
    }
}

export const TOGGLE_DONE = 'TOGGLE_DONE';
export const toggleDoneAction = (id:number): Action => {
    return {
        type: TOGGLE_DONE,
        id,
    }
}

export const SET_EXPANDED = 'SET_EXPANDED';
export const setExpandedAction = (id: number, expanded:boolean): Action => {
    return {
        type: SET_EXPANDED,
        id,
        expanded,
    }
}