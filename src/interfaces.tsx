import {DragItemTypes} from './Constants'

export interface ListItem {
    name: string;
    description?: string;
    id: number;
    children?: any[];
    parent?: number;
}

export interface Action {
    type:string,
    id?: number,
    draggedId: number,
    droppedId?: number
}

export interface DraggedItem {
    type: DragItemTypes,
    [key: string]: string | number
}

