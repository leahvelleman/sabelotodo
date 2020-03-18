
export interface list {
    name: string;
    description?: string;
    id: number;
    children?: any[];
}

export interface Item {
    name: string;
    description?: string;
    id: number;
    parent?: number;
}

export interface Action {
    type:string,
    id?: number,
    draggedId: number,
    droppedId?: number
}

