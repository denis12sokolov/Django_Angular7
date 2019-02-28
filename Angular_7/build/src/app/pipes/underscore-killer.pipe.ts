import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'underscoreKiller'
})
export class UnderscoreKillerPipe implements PipeTransform {

  transform(value: string, args?: any): string {
    return value.replace(/_/g, ' ');
  }

}
