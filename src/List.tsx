import React from 'react';
import classSet from 'react-classset';
import logo from './logo.svg';
import './List.scss';
import {list} from './interfaces'


interface ListProps {
    myList: list,
    isChild: boolean,
}

const List:React.FunctionComponent<ListProps> = (props) => {
  const {myList, isChild} = props;
  return (
    <div className={classSet({
        'List': true,
        'List--child': isChild
    })} key={myList.id}>
      <header className="List-header">
          <h1>{props.myList.name}</h1>
      </header>
      <main>
        {props.myList.description &&
            <div className="List__description">
                {myList.description}
            </div>
        }
        <ul>
            {myList.children && myList.children.map((sublist:list) => {
              return <List myList={sublist} isChild={true} key={sublist.id}/>
            })}
        </ul>
      </main>
    </div>
  );
}

export default List;
