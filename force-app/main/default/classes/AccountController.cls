public with sharing class AccountController {
  @AuraEnabled(cacheable=true)
  public static List<Account> findAccounts(String searchKey) {
    String key = '%' + searchKey + '%';
    return [SELECT Id, Name, AccountNumber FROM Account WHERE Name LIKE :key LIMIT 5];
  }

  @AuraEnabled(cacheable=true)
  public static List<Account> getAccountList() {
    return [
      SELECT Id, Name, Type, Rating, Phone, Website, AnnualRevenue
      FROM Account
      WHERE Name != NULL AND Phone != NULL AND Type != NULL AND AnnualRevenue != NULL
      LIMIT 3
    ];
  }

  @AuraEnabled(cacheable=true)
  public static List<Account> getAccounts() {
    return [SELECT Id, Name, AccountNumber, Fax FROM Account ORDER BY createdDate DESC];
  }

  @AuraEnabled(cacheable=true)
public static Account getAccountById(Id accountId) {
    return [SELECT Id, Name, AccountNumber, Type, Rating, Phone, Website, AnnualRevenue, Fax 
            FROM Account 
            WHERE Id = :accountId 
            LIMIT 1];
}

}
