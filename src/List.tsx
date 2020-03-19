import React from 'react';
import classSet from 'react-classset';
import {useDrag, DragObjectWithType} from 'react-dnd';
import './List.scss';
import {ListItem, Action} from './interfaces'
import {DragItemTypes} from './Constants'
import DropTarget from './DropTarget';


interface ListProps {
    myList: ListItem,
    isChild: boolean,
    dispatch: (arg0:Action) => void,
}

export interface DragListItemWithType extends DragObjectWithType {
    id: number,
    parentId: number,
}


const List: React.FunctionComponent<ListProps> = ({myList, isChild, dispatch}) => {
    const [{ isDragging }, drag, preview] = useDrag({
        item: { 
            type: DragItemTypes.LIST,
            id: myList.id ,
            parentId: myList.parent,
        } as DragListItemWithType,
        collect: monitor => ({
          isDragging: !!monitor.isDragging(),
        }),
      })
    return (
        <div 
            className={classSet({
                'List': true,
                'List--child': isChild,
                'List--dragging': isDragging
            })} 
            ref={preview}
            key={myList.id}   
        >
            <div className="List-dnd-target" ref={drag}></div>
            <div className="List-content">
                <header className="List-header">
                    <h1>{myList.name}</h1>
                </header>
                <main>
                    {myList.description &&
                        <div className="List__description">
                            {myList.description}
                        </div>
                    }
                    <ul>
                        {myList.children && myList.children.map((sublist: ListItem) => {
                            return <List myList={sublist} isChild={true} key={sublist.id} dispatch={dispatch}/>
                        })}
                    </ul>
                </main>
                <DropTarget dispatch={dispatch} itemId={myList.id}/>
            </div>
        </div>
    );
}

export default List;
