import React from 'react';
import classSet from 'react-classset';
import {useDrag, DragObjectWithType} from 'react-dnd';
import './List.scss';
import {ListItem, Action} from './interfaces'
import {DragItemTypes} from './Constants'
import DropTarget from './DropTarget';
import { toggleDoneAction, setExpandedAction } from './itemActions';


interface ListProps {
    myList: ListItem,
    isChild: boolean,
    dispatch: (arg0:Action) => void,
    depth?: number,
    parentIds: number[],
}

export interface DragListItemWithType extends DragObjectWithType {
    id: number,
    parentId?: number,
}


const List: React.FunctionComponent<ListProps> = ({myList, isChild, dispatch, depth=0, parentIds}) => {
    const [{ isDragging }, drag, preview] = useDrag({
        item: { 
            type: DragItemTypes.LIST,
            id: myList.id,
            parentId: myList.parent,
        } as DragListItemWithType,
        collect: monitor => ({
          isDragging: !!monitor.isDragging(),
        }),
      })
    const depthClass = `List--depth-${depth}`;
    return (
        <React.Fragment>
        <div 
            className={classSet({
                'List': true,
                'List--child': isChild,
                'List--dragging': isDragging,
                'List--done': myList.done,
                [depthClass]: true
            })} 
            ref={preview}
            key={myList.id}   
        >
            <div className="List-dnd-target" ref={drag}></div>
            <div className="List-content">
                <header className="List-header">
                 <h1>
                    <span 
                        className="List__expand-arrow" 
                        onClick={() => dispatch(setExpandedAction(myList.id, !myList.expanded))}
                        data-testid="list-expanded"
                    >
                        {myList.children && (myList.expanded? '⯆' : '⯈')}
                    </span> 
                    {myList.name}
                    <input 
                        type='checkbox' 
                        onChange={() => dispatch(toggleDoneAction(myList.id))}
                        data-testid={`done-checkbox-${myList.id}`}
                        className='List__done-checkbox'
                        checked={myList.done}
                    />
                </h1>
                </header>
                <main>
                </main>
            </div>
        </div>
        <DropTarget 
            dispatch={dispatch} 
            itemId={myList.id} 
            depth={depth + 1} 
            parentIds={parentIds}
        />
        {myList.children && myList.expanded && myList.children.map((sublist: ListItem) => {
            return <List 
                        myList={sublist} 
                        isChild={true} 
                        key={sublist.id} 
                        dispatch={dispatch}
                        depth={depth+1}
                        parentIds={parentIds.concat([myList.id])}
                    />
        })}
        </React.Fragment>
    );
}

export default List;
