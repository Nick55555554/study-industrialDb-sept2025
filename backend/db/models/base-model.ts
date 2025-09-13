import { Model as ObjectionModel } from 'objection';
import { Knex } from 'knex';

let knexInstance: Knex;

export function initializeKnex(knex: Knex) {
  knexInstance = knex;
  ObjectionModel.knex(knex);
}

export class Model extends ObjectionModel {
  static readonly tableName: string;
  static readonly idColumn: string;

  static rawColumnName<N extends string>(name: N): string {
    return `${this.tableName}.${name}`;
  }

}